import math

import networkx as nx

from utils.graphutils import compute_support, compute_influential_score
from offline.partitioning import graph_partitioning

SEED = 2023
R_MAX = 3
# PRE_THETA_LIST = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
PRE_THETA_LIST = [0.2]
BLOCK_SIZE = 4096

ALL_KEYWORD_NUM = 10000


def execute_offline(data_graph: nx.Graph) -> (nx.Graph, list):
    # 1. keyword hash for each vertex
    for i in range(data_graph.number_of_nodes()):
        # bv = BitVector(size=ALL_KEYWORD_NUM)
        bv = 0
        # 1.1 hash keywords to BV for each vertex
        for keyword in data_graph.nodes[i]["keywords"]:
            bv = bv | (1 << keyword)
        # 1.2 save BV into R
        data_graph.nodes[i]["R"] = [{
            "BV_r": 0,
            "ub_sup_r": 0,
            "Inf_ub": dict(zip(PRE_THETA_LIST, [0 for _ in PRE_THETA_LIST]))
        } for _ in range(R_MAX)]
        # print("Start to save BV as integer")
        data_graph.nodes[i]["BV"] = bv
        # print("End to save BV as integer")

        # 2. compute the edge support in each hop(v_i, r_max)
        # 2.1. compute hop(v_i, r_max)
        hop_v_r_max = nx.ego_graph(G=data_graph, n=i, radius=R_MAX, center=True)
        # 2.2. compute the support on the copy of hop(v_i, r_max)
        hop_v_r_max_with_support = compute_support(graph=hop_v_r_max)
        # 2.3. updating ub_sup in origin graph if necessary
        for (u, v) in hop_v_r_max.edges:
            if "ub_sup" not in data_graph.edges[u, v]:
                data_graph.edges[u, v]["ub_sup"] = 0
            if data_graph.edges[u, v]["ub_sup"] < hop_v_r_max_with_support.edges[u, v]["ub_sup"]:
                data_graph.edges[u, v]["ub_sup"] = hop_v_r_max_with_support.edges[u, v]["ub_sup"]
    print("BV and ub_sup is computed")
    # 3. compute r-hop and R for each r in [1, r_max] and each vertex
    for i in range(data_graph.number_of_nodes()):
        for r in range(R_MAX):  # [1, r_max]
            # 3.0. compute hop(v_i, r)
            hop_v_r = nx.ego_graph(G=data_graph, n=i, radius=r+1, center=True)
            # 3.1. compute bv_r = all BV on vertices in hop(v_i, r)
            for node_j in hop_v_r.nodes:  # int bit-or int
                data_graph.nodes[i]["R"][r]["BV_r"] = data_graph.nodes[i]["R"][r]["BV_r"] | hop_v_r.nodes[node_j]["BV"]
            # 3.2. compute ub_sup_r = max support of all edges in hop(v_i, r)
            for (u, v) in hop_v_r.edges:
                if hop_v_r.edges[u, v]["ub_sup"] > data_graph.nodes[i]["R"][r]["ub_sup_r"]:
                    data_graph.nodes[i]["R"][r]["ub_sup_r"] = hop_v_r.edges[u, v]["ub_sup"]
            # 3.3 compute influential score of hop(v_i,r) for each theta
            for theta_z in PRE_THETA_LIST:
                sigma_z = compute_influential_score(seed_community=hop_v_r, data_graph=data_graph, threshold=theta_z)
                data_graph.nodes[i]["R"][r]["Inf_ub"][theta_z] = sigma_z
    print("Synopsis for each vertex is computed")
    # 4. compute the child num for each partition: (4K - size of R) / size of pointers
    num_partition = math.floor((4096 - R_MAX * ((ALL_KEYWORD_NUM/8) + 8 + len(PRE_THETA_LIST)*8*2)) / 8)
    # 5. partitioning the graph and contructing the index
    index_root = graph_partitioning(data_graph=data_graph, num_partition=num_partition)
    print("index_root", index_root)
    return data_graph, index_root


if __name__ == "__main__":
    edge_list = [
        (0, 1, 0.9),
        (1, 2, 0.9),
        (1, 3, 0.9),
        (2, 3, 0.9),
        (3, 4, 0.9),
        (3, 5, 0.9),
        (4, 5, 0.9),
        (4, 6, 0.9),
        (4, 7, 0.9),
        (5, 6, 0.9),
        (5, 7, 0.9),
        (6, 7, 0.9)
    ]
    keywords_attr = {
        0: {"keywords": [0, 1]},
        1: {"keywords": [2, 3]},
        2: {"keywords": [3]},
        3: {"keywords": [2]},
        4: {"keywords": [0, 2]},
        5: {"keywords": [0, 3]},
        6: {"keywords": [1, 3]},
        7: {"keywords": [1, 2]}
    }
    data_graph = nx.Graph()
    data_graph.add_nodes_from(range(8))
    data_graph.add_weighted_edges_from(edge_list)
    nx.set_node_attributes(data_graph, keywords_attr)
    execute_offline(data_graph)

    # args = args_parser()
    # data_graph = data_graph_read(args.input)
    # root_index, data_graph = execute_offline(data_graph=data_graph)
    # if args.save_mid:
    #     mid_graph_save(data_graph=data_graph, index=root_index, dataset_path=args.dataset)
