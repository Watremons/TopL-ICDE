
import random
import copy
import os

import numpy as np
import networkx as nx

from utils import create_folder


def generate_dataset(seed: int, node_num: int, neighbor_num: int, add_edge_probability: float, keyword_set_size: int):
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

    # 2.2 Add the keyword set for each vertex
    keyword_set = ["sports", "shopping", "programming", "study", "reading", "writing", "e-sports", "series", "traveling", "music"]
    label_counter = [0 for _ in range(keyword_set_size)]
    for i in range(target_graph.number_of_nodes()):
        keyword_num = np.random.randint(1, keyword_set_size+1)
        keyword_idxs = random.sample(range(0, 10), keyword_num)
        keywords = []
        for idx in keyword_idxs:
            keywords.append(keyword_set[idx])
            label_counter[idx] += 1
        target_graph.nodes[i]['keywords'] = keywords

    print([{keyword_set[i]: label_counter[i]} for i in range(keyword_set_size)])

    # 3. Save the graph as ".gpickle.gz" into a folder
    folder_name = os.path.join("dataset", '{0}-{1}-{2}'.format(node_num, edges_num, keyword_set_size))
    create_folder(folder_name=folder_name)
    os.chdir(folder_name)  # Switch path to the folder
    nx.write_gpickle(target_graph, 'data_graph.gpickle.gz')


if __name__ == "__main__":
    # Set the parameters to generate dataset.
    seed = 2022
    generate_dataset(
        seed=seed,
        node_num=1000000,
        neighbor_num=5,
        add_edge_probability=0.250185,
        keyword_set_size=10
    )
