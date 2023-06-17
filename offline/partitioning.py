import os
import numpy as np
import pymetis
import networkx as nx
from BitVector import BitVector

R_MAX = os.getenv('R_MAX')
ALL_KEYWORD_NUM = os.getenv('ALL_KEYWORD_NUM')
PRE_THETA_LIST = os.getenv('PRE_THETA_LIST')
BLOCK_SIZE = os.getenv('BLOCK_SIZE')


def graph_partitioning(data_graph: nx.Graph, num_partition: int) -> list:
    # Return: size of data_graph is smaller than num_partition
    if data_graph.number_of_nodes() < num_partition:
        return [
            {
                "P": node[0],  # node index
                "R": node[1]["R"]  # node synopsis
            } for node in data_graph.nodes(data=True)
        ]

    # 0. initialize the data format
    adjacency_list = []
    for node in data_graph.nodes():
        adjacency_list.append(np.array(list(data_graph.neighbors(node))))
    # 1. do partitioning by METIS
    n_cuts, membership = pymetis.part_graph(num_partition,
                                            adjacency=adjacency_list)
    # 2. print cut result
    print('Edge Cuts: ', n_cuts)
    # 3. processing each partition
    partitions = []
    aggregated_synopsis = [{
        "BV_r": BitVector(size=ALL_KEYWORD_NUM),
        "ub_sup_r": 0,
        "Inf_ub": zip(PRE_THETA_LIST, [0 for _ in PRE_THETA_LIST])
    } for _ in range(R_MAX)]
    for i in range(num_partition):
        # 3.1. extract nodes of this partition and compute its adjacency_list
        partition_nodes = np.argwhere(np.array(membership) == i).ravel()
        partition_subgraph = nx.subgraph(data_graph, partition_nodes)
        print(partition_subgraph)
        print(nx.is_connected(partition_subgraph))
        # 3.2. Traverse to the subgraph of this partition,return the aggregated synopsis
        partition = graph_partitioning(data_graph=partition_subgraph, num_partition=num_partition)
        # data form as follows:
        # [{
        #     "P": index_node,
        #     "R": [{
        #         "BV_r": BitVector(size=ALL_KEYWORD_NUM),
        #         "ub_sup_r": 0,
        #         "Inf_ub": {}
        #         } for _ in range(R_MAX+1)]
        # } for child in partition.children]

        # 3.3. Aggregate the synopsis of children
        for turn in range(R_MAX):
            r = turn + 1
            for child_entry in partition:
                # 3.3.1. compute bv_r = all BV on vertices in children partition
                aggregated_synopsis["R"][r]["BV_r"] = aggregated_synopsis["R"][r]["BV_r"] | child_entry["R"][r]["BV_r"]
                # 3.3.2. compute bv_r =  max support of all edges in children partition
                if aggregated_synopsis["R"][r]["ub_sup_r"] < child_entry["R"][r]["ub_sup_r"]:
                    aggregated_synopsis["R"][r]["ub_sup_r"] = child_entry["R"][r]["ub_sup_r"]
                # 3.3.3 compute max \sigma_z on vertices in children partition under each \theta_z
                for theta_z in PRE_THETA_LIST:
                    if aggregated_synopsis["R"][r]["Inf_ub"][theta_z] < child_entry[i]["R"][r]["Inf_ub"][theta_z]:
                        aggregated_synopsis["R"][r]["Inf_ub"][theta_z] = child_entry[i]["R"][r]["Inf_ub"][theta_z]

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
            "P": partition,  # partition
            "R": aggregated_synopsis  # aggregated synopsis
        } for partition in partitions
    ]
