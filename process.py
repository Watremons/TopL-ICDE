import heapq

from BitVector import BitVector
import networkx as nx

from utils.graphutils import compute_influential_score

SEED = 2023
R_MAX = 3
# PRE_THETA_LIST = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
PRE_THETA_LIST = [0.2]
BLOCK_SIZE = 4096

ALL_KEYWORD_NUM = 10000


def is_pass_pruning_entry(entry: dict):
    pass


def min_score_entry(entry_set: set):
    min_seed_community = ""
    min_sigma = float("inf")
    for (seed_community_g, sigma_g) in entry_set:
        if sigma_g < min_sigma:
            min_sigma = sigma_g
            min_seed_community = seed_community_g
    return min_seed_community, min_sigma


def execute_online(
    data_graph: nx.Graph,
    query_keyword_Q: list,
    query_support_k: int,
    radius_r: int,
    threshold_theta: float,
    query_L: int,
    index_root: list,
):
    # 0. initialization:
    # 0.1 hash the query keywords set Q
    q_bv = BitVector(size=ALL_KEYWORD_NUM)
    for keyword in query_keyword_Q:
        q_bv[keyword] = 1
    # 0.2 init a maximum heap H in the form of (N, key)
    max_heap_H = [(0, index_root)]  # set value to -1*value to use the heapq
    # 0.3 init result set S, result set size counter, sigma_L
    result_set_S = set()
    sigma_L = -1  # because of the value in max_heap_H is minus
    # 0.4 compute the theta_z
    theta_z = 0
    for theta in PRE_THETA_LIST:
        if theta > threshold_theta:
            break
        theta_z = theta
    # 1. Index traversal
    while len(max_heap_H) > 0:
        heapq.heapify(max_heap_H)
        (key, index_N) = heapq.heappop(max_heap_H)
        if (-1*key) <= sigma_L:
            break
        if len(index_N) > 0:
            if index_N[0]["T"]:  # N is a leaf node with child entry made by vertex
                for vertex_entry_i in index_N:
                    if is_pass_pruning_entry(vertex_entry_i):  # check the community-level pruning
                        hop_v_i_r = nx.ego_graph(G=data_graph, n=vertex_entry_i["P"], radius=radius_r, center=True)
                        seed_community = nx.k_truss(G=hop_v_i_r, k=query_support_k)  # TODO: get all k-truss from hop_v_i_r
                        seed_community_list = [seed_community]
                        for seed_community_g in seed_community_list:
                            sigma_g = compute_influential_score(seed_community=seed_community_g, data_graph=data_graph, threshold=threshold_theta)
                            if len(result_set_S) < query_L:  # add to result set if size is less than L
                                result_set_S.add((seed_community_g, sigma_g))
                                if len(result_set_S) == query_L:
                                    _, min_sigma = min_score_entry(result_set_S)
                                    sigma_L = min_sigma
                            else:  # if size is greater than L
                                if sigma_g > sigma_L:  # add to result set and remove the smallest one
                                    result_set_S.add(seed_community_g, sigma_g)
                                    min_seed_community, min_sigma = min_score_entry(result_set_S)
                                    sigma_L = min_sigma
                                    result_set_S.remove((min_seed_community, min_sigma))
            else:  # N is non-leaf node with child entry made by index node
                for child_entry in index_N:
                    if is_pass_pruning_entry(child_entry):  # check the community-level pruning
                        max_heap_H.append((child_entry["P"], child_entry["R"][radius_r]["Inf_ub"][theta_z]))
    return result_set_S


# Index Node:
# [{
#     "P": index_node,
#     "R": [{
#         "BV_r": BitVector(size=ALL_KEYWORD_NUM),
#         "ub_sup_r": 0,
#         "Inf_ub": {}
#         } for _ in range(R_MAX)],
#     "T": True/False
# } for child in partition.children]
