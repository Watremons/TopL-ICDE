import numpy as np
import pymetis
import networkx as nx

R_MAX = 3
PRE_THETA_LIST = [0.05, 0.08, 0.1]
# PRE_THETA_LIST = [0.08]
# PRE_THETA_LIST = [0.2]


def graph_partitioning(data_graph: nx.Graph, num_partition: int, level: int) -> list:
    # print()
    # print("Start partitioning to", num_partition, ":")
    # print(data_graph)
    # print(data_graph.nodes)
    # print(data_graph.edges)
    # Return: size of data_graph is smaller than num_partition
    if data_graph.number_of_nodes() < num_partition:
        return [
            {
                "P": node[0],       # node index
                "R": node[1]["R"],  # node synopsis
                "T": True,          # leaf node
                "L": level           # level
            } for node in data_graph.nodes(data=True)
        ]

    # 0. initialize the data format
    # key: old graph, value: new graph
    vertex_index_mapping = dict(zip([node for node in data_graph.nodes()], [i for i in range(data_graph.number_of_nodes())]))
    adjacency_list = []
    for node in data_graph.nodes():
        adjacency_list.append(np.array([vertex_index_mapping[neighbor] for neighbor in data_graph.neighbors(node)]))
    # 1. do partitioning by METIS
    n_cuts, membership = pymetis.part_graph(num_partition,
                                            adjacency=adjacency_list)
    # 2. print cut result
    # print('Edge Cuts: ', n_cuts)
    # 3. processing each partition
    partitions = []
    aggregated_synopsis = [{
        "BV_r": 0,
        "ub_sup_r": 0,
        "Inf_ub": dict(zip(PRE_THETA_LIST, [0 for _ in PRE_THETA_LIST]))
    } for _ in range(R_MAX)]
    # key: new graph, value: old graph
    reverse_vertex_index_mapping = dict(zip(vertex_index_mapping.values(), vertex_index_mapping.keys()))
    for i in range(num_partition):
        # 3.1. extract nodes of this partition and compute its adjacency_list
        partition_nodes_raw = np.argwhere(np.array(membership) == i).ravel()
        # print("partition_nodes_raw", len(partition_nodes_raw), partition_nodes_raw)
        partition_nodes = [reverse_vertex_index_mapping[node] for node in partition_nodes_raw]
        # print("partition_nodes", len(partition_nodes), partition_nodes)
        # print("data_graph.nodes", data_graph.nodes)
        partition_subgraph = nx.subgraph(data_graph, partition_nodes)
        # print("partition_subgraph", partition_subgraph)
        # print(nx.is_connected(partition_subgraph))
        # 3.2. Traverse to the subgraph of this partition,return the aggregated synopsis
        partition = graph_partitioning(data_graph=partition_subgraph, num_partition=num_partition, level=level+1)
        # data form as follows:
        # [{
        #     "P": index_node,
        #     "R": [{
        #         "BV_r": 0,
        #         "ub_sup_r": 0,
        #         "Inf_ub": {}
        #         } for _ in range(R_MAX)],
        #     "T": True/False
        # } for child in partition.children]

        # 3.3. Aggregate the synopsis of children
        for r in range(R_MAX):
            for child_entry in partition:
                # 3.3.1. compute bv_r = all BV on vertices in children partition
                aggregated_synopsis[r]["BV_r"] = aggregated_synopsis[r]["BV_r"] | child_entry['R'][r]["BV_r"]
                # 3.3.2. compute bv_r =  max support of all edges in children partition
                if aggregated_synopsis[r]["ub_sup_r"] < child_entry['R'][r]["ub_sup_r"]:
                    aggregated_synopsis[r]["ub_sup_r"] = child_entry['R'][r]["ub_sup_r"]
                # 3.3.3 compute max \sigma_z on vertices in children partition under each \theta_z
                for theta_z in PRE_THETA_LIST:
                    if aggregated_synopsis[r]["Inf_ub"][theta_z] < child_entry['R'][r]["Inf_ub"][theta_z]:
                        aggregated_synopsis[r]["Inf_ub"][theta_z] = child_entry['R'][r]["Inf_ub"][theta_z]

        # 扩展
        # nodes = set(partition_subgraph.nodes)
        # for node in partition_subgraph.nodes:
        #     extend_nodes = list(
        #         nx.bfs_tree(data_graph, node, depth_limit=1))
        #     nodes = nodes | set(extend_nodes)
        # 去重
        # print(len(nodes))
        # nodes = list(nodes)
        # part_extend = nx.subgraph(data_graph, nodes)
        # print(part_extend)
        # print(nx.is_connected(part_extend))

        partitions.append(partition)
    return [
        {
            "P": partition,            # partition
            "R": aggregated_synopsis,  # aggregated synopsis
            "T": False,                # leaf node
            "L": level
        } for partition in partitions
    ]
