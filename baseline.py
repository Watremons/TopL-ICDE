import time
import numpy as np
import os
import networkx as nx

from utils.argparser import args_parser
from utils.graphutils import compute_influential_score
from utils.ioutils import data_graph_read, result_graph_save, statistic_file_save
from online.statistics import Statistics


def execute_baseline(
    data_graph: nx.Graph,
    query_keyword_Q: list,
    query_support_k: int,
    radius_r: int,
    threshold_theta: float,
    query_L: int,
    stat: Statistics
) -> list:
    # 0. Sample nodes from the whole map following Uniform distribution
    result_set_S = set()
    sample_vertices_index_list = np.random.choice(data_graph.nodes, data_graph.number_of_nodes()//1000, replace=False)
    # sample_vertices_index_list = list(data_graph.nodes)
    for node in sample_vertices_index_list:
        # print("Now node:", node)
        # 1. compute hop(node, radius_r)
        compute_r_hop_start_timestamp = time.time()
        hop_node_r = nx.ego_graph(G=data_graph, n=node, radius=radius_r, center=True)
        stat.compute_r_hop_time += (time.time() - compute_r_hop_start_timestamp)
        # 2. decompose a k-truss
        compute_k_truss_start_timestamp = time.time()
        # seed_community_g = compute_k_truss(graph=hop_v_i_r, k=query_support_k)  # get all k-truss from hop_v_i_r
        seed_community_g = nx.k_truss(G=hop_node_r, k=query_support_k)
        stat.compute_k_truss_time += (time.time() - compute_k_truss_start_timestamp)
        if seed_community_g.number_of_nodes() == 0 or seed_community_g.nodes in [result[0].nodes for result in result_set_S]:  # Delete the same community
            continue
        # 3. check the keywords
        flag = True
        for node in seed_community_g.nodes(data=True):
            if set(node[1]["keywords"]) & set(query_keyword_Q) == 0:
                flag = False
                break
        if not flag:
            continue
        # 4. compute influential scores
        compute_influential_score_start_timestamp = time.time()
        sigma_g = compute_influential_score(seed_community=seed_community_g, data_graph=data_graph, threshold=threshold_theta)
        stat.compute_influential_score_time += (time.time() - compute_influential_score_start_timestamp)
        # 5. add result to set
        modify_result_set_start_timestamp = time.time()
        result_set_S.add((seed_community_g, sigma_g))
        # print("Add:", (seed_community_g, sigma_g))
        stat.modify_result_set_time += (time.time() - modify_result_set_start_timestamp)

    return sorted(list(result_set_S), key=lambda s: s[1], reverse=True)[0:query_L]


if __name__ == "__main__":
    args = args_parser()
    stat = Statistics(
        input_file_folder=args.input,
        query_keyword_Q=[int(keyword) for keyword in args.keywords.split(",")],
        query_support_k=args.support,
        radius_r=args.radius,
        threshold_theta=args.theta,
        query_L=args.top,
    )
    print("Start file read:")
    data_graph = data_graph_read(args.input)
    print("Start baseline processing:")
    stat.start_timestamp = time.time()
    result_set = execute_baseline(
        data_graph=data_graph,
        query_keyword_Q=[int(keyword) for keyword in args.keywords.split(",")],
        query_support_k=args.support,
        radius_r=args.radius,
        threshold_theta=args.theta,
        query_L=args.top,
        stat=stat
    )
    stat.finish_timestamp = time.time()
    stat.solver_result = list(result_set)
    for result in result_set:
        print(result[0], result[1])
    result_graph_save(result_graph=[result[0] for result in result_set], dataset_path=os.path.join(args.input, 'baseline'))
    statistic_file_save(stat=stat, dataset_path=os.path.join(args.input, 'baseline'))
    print(stat.generate_stat_result())
