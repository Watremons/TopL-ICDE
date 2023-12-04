import os
import random
import numpy as np
import pymetis
import networkx as nx

all_keyword_num = 10
keywords_per_vertex_num = 3
partition_num = 1

if __name__ == "__main__":
    graph_path = os.path.join(os.path.dirname(__file__), "data_graph.gpickle.gz")
    data_graph = nx.read_gpickle(graph_path)
    vertex_index_mapping = dict(zip([node for node in data_graph.nodes()], [i for i in range(data_graph.number_of_nodes())]))
    adjacency_list = []
    for node in data_graph.nodes():
        adjacency_list.append(np.array([vertex_index_mapping[neighbor] for neighbor in data_graph.neighbors(node)]))

    n_cuts, membership = pymetis.part_graph(partition_num, adjacency=adjacency_list)
    # key: new graph, value: old graph
    reverse_vertex_index_mapping = dict(zip(vertex_index_mapping.values(), vertex_index_mapping.keys()))
    data_subgraph = dict()
    for i in range(partition_num):
        # extract nodes of this partition and compute its adjacency_list
        partition_nodes_raw = np.argwhere(np.array(membership) == 0).ravel()
        # print("partition_nodes_raw", len(partition_nodes_raw), partition_nodes_raw)
        partition_nodes = [reverse_vertex_index_mapping[node] for node in partition_nodes_raw]
        # print("partition_nodes", len(partition_nodes), partition_nodes)
        # print("data_graph.nodes", data_graph.nodes)
        data_subgraph = nx.subgraph(data_graph, partition_nodes)
    print("data_subgraph", data_subgraph)
    print(
        "{0}-{1}-{2}-{3}".format(
            data_subgraph.number_of_nodes(),
            data_subgraph.number_of_edges(),
            all_keyword_num,
            keywords_per_vertex_num
        )
    )
    # Re-distribute the keyword set to each vertex
    keywords_set = range(0, all_keyword_num)
    label_counter = [0 for _ in range(all_keyword_num)]
    for i in data_subgraph.nodes:
        data_subgraph.nodes[i].clear()
        keyword_num = np.random.randint(max(keywords_per_vertex_num-1, 1), keywords_per_vertex_num+2)  # the num is key_per ± 1
        keywords = random.sample(keywords_set, keyword_num)
        for keyword in keywords:
            label_counter[keyword] += 1
        data_subgraph.nodes[i]['keywords'] = keywords
    # Recompute the edge data
    for i in data_subgraph.nodes:
        for neighbor in data_subgraph.neighbors(i):
            data_subgraph.edges[i, neighbor]["weight"] = random.uniform(0.5, 0.6)
    nx.write_gpickle(data_subgraph, 'data_subgraph.gpickle.gz')
