import heapq
import time
import math
import networkx as nx

from utils.graphutils import compute_influential_score, compute_hop_v_r
from online.statistics import Statistics

SEED = 2023
R_MAX = 2
# PRE_THETA_LIST = [0.1, 0.2, 0.3]
PRE_THETA_LIST = [0.2]


def is_pass_pruning_entry(entry: dict, radius: int, query_bv: int, query_support: int, theta_z: float, sigma_L: float):
    # {
    #     "P": index_node,
    #     "R": [{
    #         "BV_r": 0,
    #         "ub_sup_r": 0,
    #         "Inf_ub": {}
    #         } for _ in range(R_MAX)],
    #     "T": True/False
    # }
    synopsis = entry["R"][radius]
    # if synopsis["BV_r"] & query_bv != query_bv:  # (Index-Level) Keyword Pruning
    if synopsis["BV_r"] & query_bv == 0:  # (Index-Level) Keyword Pruning
        return False
    if synopsis["ub_sup_r"] < query_support:  # (Index-Level) Support Pruning
        return False
    if synopsis["Inf_ub"][str(theta_z)] < sigma_L:  # (Index-Level) Influential Score Pruning
        return False
    return True


class IndexEntry:
    def __init__(self, key, index_N, idx):
        self.key = key
        self.index_N = index_N
        self.idx = idx

    def __lt__(self, other):
        if self.index_N["L"] == other.index_N["L"]:
            if math.fabs(self.key - other.key) < 0.0001:
                return self.idx < self.idx
            else:
                return self.key < other.key
        else:
            return self.index_N["L"] > other.index_N["L"]


def min_score_entry(entry_set: set):
    min_seed_community = ""
    min_sigma = float("inf")
    for (seed_community_g, sigma_g, influenced_community_g_inf) in entry_set:
        if sigma_g < min_sigma:
            min_sigma = sigma_g
            min_seed_community = seed_community_g
            min_influenced_community_g_inf = influenced_community_g_inf
    return min_seed_community, min_sigma, min_influenced_community_g_inf


def execute_online(
    data_graph: nx.Graph,
    query_keyword_Q: list,
    query_support_k: int,
    radius_r: int,
    threshold_theta: float,
    query_L: int,
    nlparam: int,
    index_root: list,
    stat: Statistics
) -> (set, int):
    # 0. initialization:
    # 0.1 hash the query keywords set Q
    q_bv = 0
    for keyword in query_keyword_Q:
        q_bv = q_bv | (1 << keyword)
    # 0.2 init result set S, result set size counter, sigma_L
    result_set_S = set()
    sigma_L = -1  # because of the value in max_heap_H is minus
    # 0.3 compute the theta_z
    theta_z = PRE_THETA_LIST[0]
    for theta in PRE_THETA_LIST:
        if theta > threshold_theta:
            break
        theta_z = theta
    # 0.4. trans radius to radius index
    radius_r_idx = radius_r - 1
    # 0.5 init a maximum heap H in the form of (N, key)
    max_heap_H = []  # set value to -1*value to use the heapq
    for idx, entry in enumerate(index_root):
        heapq.heappush(max_heap_H, IndexEntry(key=(-1)*entry["R"][radius_r_idx]["Inf_ub"][str(theta_z)], index_N=entry, idx=idx))
    # 0.6 set the L to n*L
    query_nL = nlparam * query_L
    print("query_nL", query_nL)
    vertex_pruning_counter = 0
    leaf_node_visit_counter = 0
    entry_pruning_counter = 0
    max_k_truss_cost = 0
    max_influential_score_cost = 0
    # 1. Index traversal
    while len(max_heap_H) > 0:
        start_timestamp = time.time()
        now_entry = heapq.heappop(max_heap_H)
        heapq.heapify(max_heap_H)
        stat.select_greatest_entry_in_H_time += (time.time() - start_timestamp)

        # print("Now Level:", now_entry.index_N["L"])
        # print("now key:", (-1)*now_entry.key, "smaller than", sigma_L)
        if ((-1)*now_entry.key) <= sigma_L:
            print("early termination")
            break
        for child_entry in now_entry.index_N['P']:
            if child_entry['T']:  # N is a leaf node with child entry made by vertex
                leaf_node_start_timestamp = time.time()
                if is_pass_pruning_entry(entry=child_entry, radius=radius_r_idx, query_bv=q_bv, query_support=query_support_k-2, theta_z=theta_z, sigma_L=sigma_L):  # check the community-level pruning
                    compute_r_hop_start_timestamp = time.time()
                    # hop_v_i_r = nx.ego_graph(G=data_graph, n=child_entry["P"], radius=radius_r, center=True)
                    hop_v_i_r = compute_hop_v_r(graph=data_graph, node_v=child_entry["P"], radius=radius_r)
                    stat.compute_r_hop_time += (time.time() - compute_r_hop_start_timestamp)
                    compute_k_truss_start_timestamp = time.time()
                    # seed_community_g = compute_k_truss(graph=hop_v_i_r, k=query_support_k-2)  # get all k-truss from hop_v_i_r
                    seed_community_g = nx.k_truss(G=hop_v_i_r, k=query_support_k)
                    if max_k_truss_cost < (time.time() - compute_k_truss_start_timestamp):
                        max_k_truss_cost = (time.time() - compute_k_truss_start_timestamp)
                    stat.compute_k_truss_time += (time.time() - compute_k_truss_start_timestamp)
                    if seed_community_g.number_of_nodes() == 0 or seed_community_g.nodes in [result[0].nodes for result in result_set_S]:  # Delete the same community
                        continue
                    flag = True
                    for vertex in seed_community_g.nodes(data=True):
                        if q_bv & vertex[1]["BV"] == 0:
                            flag = False
                            break
                    if not flag:
                        continue
                    # bv_g = 0
                    # for vertex in seed_community_g.nodes(data=True):
                    #     bv_g = bv_g | vertex[1]["BV"]
                    # if bv_g & q_bv != q_bv:
                    #     continue
                    vertex_pruning_counter += 1
                    compute_influential_score_start_timestamp = time.time()
                    sigma_g, influenced_community_g_inf = compute_influential_score(seed_community=seed_community_g, data_graph=data_graph, threshold=threshold_theta)
                    if max_influential_score_cost < (time.time() - compute_influential_score_start_timestamp):
                        max_influential_score_cost = (time.time() - compute_influential_score_start_timestamp)
                    stat.compute_influential_score_time += (time.time() - compute_influential_score_start_timestamp)
                    modify_result_set_start_timestamp = time.time()
                    # print(seed_community_g)
                    if len(result_set_S) < query_nL:  # add to result set if size is less than L
                        result_set_S.add((seed_community_g, sigma_g, influenced_community_g_inf))
                        if len(result_set_S) == query_nL:
                            _, min_sigma, _ = min_score_entry(result_set_S)
                            sigma_L = min_sigma
                            # print("Now got Top L and sigma_L is", sigma_L)
                    else:  # if size is greater than L
                        if sigma_g > sigma_L:  # add to result set and remove the smallest one
                            # print("Now got new top L", sigma_g, " and sigma_L is", sigma_L)
                            result_set_S.add((seed_community_g, sigma_g, influenced_community_g_inf))
                            min_seed_community, min_sigma, influenced_community_g_inf = min_score_entry(result_set_S)
                            sigma_L = min_sigma
                            result_set_S.remove((min_seed_community, min_sigma, influenced_community_g_inf))
                    stat.modify_result_set_time += (time.time() - modify_result_set_start_timestamp)

                stat.leaf_node_traverse_time += (time.time() - leaf_node_start_timestamp)
            else:  # N is non-leaf node with child entry made by index node
                nonleaf_node_start_timestamp = time.time()
                if is_pass_pruning_entry(entry=child_entry, radius=radius_r_idx, query_bv=q_bv, query_support=query_support_k-2, theta_z=theta_z, sigma_L=sigma_L):  # check the community-level pruning
                    heapq.heappush(max_heap_H, IndexEntry((-1)*child_entry["R"][radius_r_idx]["Inf_ub"][str(theta_z)], child_entry, idx))
                    if len(child_entry["P"]) == 0 or child_entry["P"][0]["T"]:
                        leaf_node_visit_counter += 1
                else:
                    # print("An entry on level", vertex_entry_i["L"], "is pruned")
                    entry_pruning_counter += 1
                stat.nonleaf_node_traverse_time += (time.time() - nonleaf_node_start_timestamp)

    stat.vertex_pruning_counter = (data_graph.number_of_nodes() - vertex_pruning_counter)
    stat.entry_pruning_counter = entry_pruning_counter
    stat.leaf_node_visit_counter = leaf_node_visit_counter
    # print("Max k truss cost:", max_k_truss_cost)
    # print("Max score cost:", max_influential_score_cost)

    # print(data_graph.nodes(data=True))
    sum_influential_score = 0
    for seed_community in result_set_S:
        print(seed_community[0].nodes)
        sum_influential_score += seed_community[1]

    return result_set_S, sum_influential_score


# Index Node:
# [{
#     "P": index_node,
#     "R": [{
#         "BV_r": 0,
#         "ub_sup_r": 0,
#         "Inf_ub": {}
#         } for _ in range(R_MAX)],
#     "T": True/False
# } for child in partition.children]
