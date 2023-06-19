import heapq
import time

import networkx as nx

from utils.graphutils import compute_influential_score, compute_hop_v_r
from online.statistics import Statistics

SEED = 2023
R_MAX = 3
# PRE_THETA_LIST = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
PRE_THETA_LIST = [0.2]
BLOCK_SIZE = 4096

ALL_KEYWORD_NUM = 10000


def is_pass_pruning_entry(entry: dict, radius: int, query_bv: int, query_support: int, theta_z: float, sigma_L: float):
    # {
    #     "P": index_node,
    #     "R": [{
    #         "BV_r": BitVector(size=ALL_KEYWORD_NUM),
    #         "ub_sup_r": 0,
    #         "Inf_ub": {}
    #         } for _ in range(R_MAX)],
    #     "T": True/False
    # }
    synopsis = entry["R"][radius]
    if synopsis["BV_r"] & query_bv == 0:  # (Index-Level) Keyword Pruning
        return False
    if synopsis["ub_sup_r"] < query_support:  # (Index-Level) Support Pruning
        return False
    if synopsis["Inf_ub"][str(theta_z)] < sigma_L:  # (Index-Level) Influential Score Pruning
        return False
    return True


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
    stat: Statistics
) -> list:
    # 0. initialization:
    # 0.1 hash the query keywords set Q
    q_bv = 0
    for keyword in query_keyword_Q:
        q_bv = q_bv | (1 << keyword)
    # 0.2 init a maximum heap H in the form of (N, key)
    max_heap_H = [(0, index_root)]  # set value to -1*value to use the heapq
    # 0.3 init result set S, result set size counter, sigma_L
    result_set_S = set()
    sigma_L = -1  # because of the value in max_heap_H is minus
    # 0.4 compute the theta_z
    theta_z = PRE_THETA_LIST[0]
    for theta in PRE_THETA_LIST:
        if theta > threshold_theta:
            break
        theta_z = theta
    # 1. Index traversal
    while len(max_heap_H) > 0:
        start_timestamp = time.time()
        (key, index_N) = heapq.nlargest(1, max_heap_H, key=lambda s: s[0])[0]
        stat.select_greatest_entry_in_H_time += (time.time() - start_timestamp)
        max_heap_H.remove((key, index_N))
        # print("Traversing index_N with", len(index_N), "entries")
        if key <= sigma_L:
            break
        if len(index_N) > 0:
            if index_N[0]['T']:  # N is a leaf node with child entry made by vertex
                leaf_node_start_timestamp = time.time()
                for vertex_entry_i in index_N:
                    if is_pass_pruning_entry(entry=vertex_entry_i, radius=radius_r, query_bv=q_bv, query_support=query_support_k, theta_z=theta_z, sigma_L=sigma_L):  # check the community-level pruning
                        compute_r_hop_start_timestamp = time.time()
                        # hop_v_i_r = nx.ego_graph(G=data_graph, n=vertex_entry_i["P"], radius=radius_r, center=True)
                        hop_v_i_r = compute_hop_v_r(graph=data_graph, node_v=vertex_entry_i["P"], radius=radius_r)
                        stat.compute_r_hop_time += (time.time() - compute_r_hop_start_timestamp)
                        compute_k_truss_start_timestamp = time.time()
                        seed_community_g = nx.k_truss(G=hop_v_i_r, k=query_support_k)  # get all k-truss from hop_v_i_r
                        stat.compute_k_truss_time += (time.time() - compute_k_truss_start_timestamp)
                        # TODO: Check the influential community
                        compute_influential_score_start_timestamp = time.time()
                        sigma_g = compute_influential_score(seed_community=seed_community_g, data_graph=data_graph, threshold=threshold_theta)
                        stat.compute_influential_score_time += (time.time() - compute_influential_score_start_timestamp)
                        modify_result_set_start_timestamp = time.time()
                        if len(result_set_S) < query_L:  # add to result set if size is less than L
                            result_set_S.add((seed_community_g, sigma_g))
                            if len(result_set_S) == query_L:
                                _, min_sigma = min_score_entry(result_set_S)
                                sigma_L = min_sigma
                        else:  # if size is greater than L
                            if sigma_g > sigma_L:  # add to result set and remove the smallest one
                                result_set_S.add((seed_community_g, sigma_g))
                                min_seed_community, min_sigma = min_score_entry(result_set_S)
                                sigma_L = min_sigma
                                result_set_S.remove((min_seed_community, min_sigma))
                        stat.modify_result_set_time += (time.time() - modify_result_set_start_timestamp)
                stat.leaf_node_traverse_time += (time.time() - leaf_node_start_timestamp)
            else:  # N is non-leaf node with child entry made by index node
                nonleaf_node_start_timestamp = time.time()
                for child_entry in index_N:
                    if is_pass_pruning_entry(entry=child_entry, radius=radius_r, query_bv=q_bv, query_support=query_support_k, theta_z=theta_z, sigma_L=sigma_L):  # check the community-level pruning
                        max_heap_H.append((child_entry["R"][radius_r]["Inf_ub"][str(theta_z)], child_entry["P"]))
                stat.nonleaf_node_traverse_time += (time.time() - nonleaf_node_start_timestamp)
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
