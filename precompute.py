import networkx as nx

from utils.graphutils import compute_support, compute_influential_score
from offline.partitioning import compute_sorted_node_list, node_list_split

R_MAX = 2
# PRE_THETA_LIST = [0.1, 0.2, 0.3]
PRE_THETA_LIST = [0.2]
BLOCK_SIZE = 4096
ALL_KEYWORD_NUM = 1000


def compute_bv_and_ub_sup(node_index: int, data_graph: nx.Graph):
    bv = 0
    # 1.1 hash keywords to BV for each vertex
    for keyword in data_graph.nodes[node_index]["keywords"]:
        bv = bv | (1 << keyword)
    # 1.2 save BV into R
    data_graph.nodes[node_index]["R"] = [{
        "BV_r": 0,
        "ub_sup_r": 0,
        "Inf_ub": dict(zip(PRE_THETA_LIST, [0 for _ in PRE_THETA_LIST]))
    } for _ in range(R_MAX)]
    # print("Start to save BV as integer")
    data_graph.nodes[node_index]["BV"] = bv
    # print("End to save BV as integer")

    # 2. compute the edge support in each hop(v_i, r_max)
    # 2.1. compute hop(v_i, r_max)
    # start_timestamp = time.time()
    hop_v_r_max = nx.ego_graph(G=data_graph, n=node_index, radius=R_MAX, center=True)
    # hop_v_r_max = compute_hop_v_r(graph=data_graph, node_v=i, radius=R_MAX)
    # print("compute r_max hop for", time.time()-start_timestamp)
    # 2.2. compute the support on the copy of hop(v_i, r_max)
    # start_timestamp = time.time()
    hop_v_r_max_with_support = compute_support(graph=hop_v_r_max)
    # print("compute support for", time.time()-start_timestamp)
    # 2.3. updating ub_sup in origin graph if necessary
    for (u, v) in hop_v_r_max.edges:
        if "ub_sup" not in data_graph.edges[u, v]:
            data_graph.edges[u, v]["ub_sup"] = 0
        if data_graph.edges[u, v]["ub_sup"] < hop_v_r_max_with_support.edges[u, v]["ub_sup"]:
            data_graph.edges[u, v]["ub_sup"] = hop_v_r_max_with_support.edges[u, v]["ub_sup"]
    # print("ub_sup is", data_graph.edges[u, v]["ub_sup"])


def compute_synopsis(node_index: int, data_graph: nx.Graph):
    for r in range(R_MAX):  # [1, r_max]
        # 3.0. compute hop(v_i, r)
        # starttime = time.time()
        hop_v_r = nx.ego_graph(G=data_graph, n=node_index, radius=r+1, center=True)
        # print("compute r-hop", time.time()-starttime)
        # hop_v_r = compute_hop_v_r(graph=data_graph, node_v=i, radius=r+1)
        # 3.1. compute bv_r = all BV on vertices in hop(v_i, r)
        # starttime = time.time()
        for node_j in hop_v_r.nodes:  # int bit-or int
            data_graph.nodes[node_index]["R"][r]["BV_r"] = data_graph.nodes[node_index]["R"][r]["BV_r"] | hop_v_r.nodes[node_j]["BV"]
        # print("compute BV_r", time.time()-starttime)
        # 3.2. compute ub_sup_r = max support of all edges in hop(v_i, r)
        # starttime = time.time()
        for (u, v) in hop_v_r.edges:
            if hop_v_r.edges[u, v]["ub_sup"] > data_graph.nodes[node_index]["R"][r]["ub_sup_r"]:
                data_graph.nodes[node_index]["R"][r]["ub_sup_r"] = hop_v_r.edges[u, v]["ub_sup"]
        # print("compute ub_sup_r", time.time()-starttime)
        # 3.3 compute influential score of hop(v_i,r) for each theta
        # last_sigma_z = 0
        for theta_z in reversed(PRE_THETA_LIST):
            sigma_z, _ = compute_influential_score(seed_community=hop_v_r, data_graph=data_graph, threshold=theta_z)
            data_graph.nodes[node_index]["R"][r]["Inf_ub"][theta_z] = sigma_z


def execute_offline(data_graph: nx.Graph) -> nx.Graph:
    # 0. save the neighbors in vertex
    for i in data_graph.nodes:
        data_graph.nodes[i]["N"] = list(data_graph.neighbors(i))
    print("neighbors N for each vertex is computed")
    # 1. keyword hash for each vertex
    for node_index, i in enumerate(data_graph.nodes):
        if (node_index+1) % 100 == 0:
            print("BV and ub_sup for node", node_index+1, "in", data_graph.number_of_nodes(), "has neighbors", len(list(data_graph.neighbors(i))))
        compute_bv_and_ub_sup(node_index=i, data_graph=data_graph)

    print("BV and ub_sup is computed")
    # 3. compute r-hop and R for each r in [1, r_max] and each vertex
    for node_index, i in enumerate(data_graph.nodes):
        if (node_index+1) % 100 == 0:
            print("BV_r, ub_sup_r and Inf_ub for node", node_index+1, "in", data_graph.number_of_nodes())
        compute_synopsis(node_index=i, data_graph=data_graph)

    print("Synopsis for each vertex is computed")
    return data_graph


def construct_index(data_graph: nx.Graph) -> list:
    # 4. compute the child num for each partition
    num_partition = 16
    # 5. compute the sorted node list with data
    sorted_node_list = compute_sorted_node_list(data_graph=data_graph)
    # for node in sorted_node_list:
    #      print(node)
    # 5. partitioning the graph and contructing the index
    # index_root = graph_partitioning(data_graph=data_graph, num_partition=num_partition, level=0)
    index_root = node_list_split(node_list=sorted_node_list, num_partition=num_partition, level=0)
    print("Graph index is computed")
    # print("index_root", index_root)
    return index_root


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
    # execute_offline(data_graph)
    print(data_graph[1])

    # args = args_parser()
    # data_graph = data_graph_read(args.input)
    # root_index, data_graph = execute_offline(data_graph=data_graph)
    # if args.save_mid:
    #     mid_graph_save(data_graph=data_graph, index=root_index, dataset_path=args.dataset)
