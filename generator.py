
import random
import copy
import os

import numpy as np
import networkx as nx

from utils.ioutils import create_folder


def generate_dataset(seed: int, keywords_per_vertex_num: int, all_keyword_num: int, node_num: int, neighbor_num: int, add_edge_probability: float):
    random.seed(seed)
    np.random.seed(seed)
    # 1. Generate a graph
    target_graph = nx.newman_watts_strogatz_graph(n=node_num, k=neighbor_num, p=add_edge_probability)
    # 1.1. Make sure the graph is connected
    while not nx.is_connected(target_graph):
        target_graph = nx.newman_watts_strogatz_graph(node_num, neighbor_num, add_edge_probability)
    # 2. Compute infos of graph
    edges_num = target_graph.number_of_edges()
    average_degree = sum(
        d for v, d in nx.degree(target_graph)) / target_graph.number_of_nodes()
    print(target_graph)
    print('Average Degree: ', average_degree)
    print('Max Degree: ', max(d for v, d in nx.degree(target_graph)))
    print('Min Degree: ', min(d for v, d in nx.degree(target_graph)))

    # 2.1. Delete some edges until edge num equals node_num * neighbor_num / 2
    while target_graph.number_of_edges() > node_num * neighbor_num / 2:
        (u, v) = random.sample(target_graph.edges, 1)[0]
        G = copy.deepcopy(target_graph)
        G.remove_edge(u, v)
        if nx.is_connected(G):
            target_graph.remove_edge(u, v)

    # Print infos
    print(nx.is_connected(target_graph))
    edges_num = target_graph.number_of_edges()
    average_degree = sum(
        d for v, d in nx.degree(target_graph)) / target_graph.number_of_nodes()
    print(target_graph)
    print('Average Degree: ', average_degree)
    print('Max Degree: ', max(d for v, d in nx.degree(target_graph)))
    print('Min Degree: ', min(d for v, d in nx.degree(target_graph)))

    # 2.2. Add the keyword set to each vertex
    keywords_set = range(0, all_keyword_num)
    label_counter = [0 for _ in range(all_keyword_num)]
    for i in range(target_graph.number_of_nodes()):
        keyword_num = np.random.randint(max(keywords_per_vertex_num-1, 0), keywords_per_vertex_num+2)  # the num is key_per ± 1
        keywords = random.sample(keywords_set, keyword_num)
        for keyword in keywords:
            label_counter[keyword] += 1
        target_graph.nodes[i]['keywords'] = keywords
        print(target_graph.nodes[i])

    # print([{keywords_set[i]: label_counter[i]} for i in range(all_keyword_num)])

    # TODO: 2.3. Add the weight (propagation probability) to each edge
    # WC model: pp(u, v) for an edge (u, v) is 1/d(v), where d(v) is the in-degree of v.
    for i in range(target_graph.number_of_nodes()):
        neighbors_num = len(list(target_graph.neighbors(i)))
        for neighbor in target_graph.neighbors(i):
            target_graph.edges[i, neighbor]["weight"] = 1 / neighbors_num
            # print(target_graph.get_edge_data(i, neighbor))
    # TRIVALENCY model: randomly select a probability from the set {0.1, 0.01, 0.001}

    # 3. Save the graph as ".gpickle.gz" into a folder, name
    folder_name = os.path.join("dataset", "manual", '{0}-{1}-{2}-{3}'.format(node_num, edges_num, all_keyword_num, keywords_per_vertex_num))
    create_folder(folder_name=folder_name)
    os.chdir(folder_name)  # Switch path to the folder
    nx.write_gpickle(target_graph, 'data_graph.gpickle.gz')
    print(folder_name, 'data_graph.gpickle.gz', "saved successfully!")


if __name__ == "__main__":
    # Set the parameters to generate dataset.
    seed = 2022
    generate_dataset(
        seed=seed,
        keywords_per_vertex_num=3,  # 1, 2, 3, 4, 5
        all_keyword_num=1000,  # 500, 800, 1K, 2K, 5K
        node_num=50000,  # 10K, 30K, 50K, 100K, 500K, 1M
        neighbor_num=5,
        add_edge_probability=0.250185
    )
