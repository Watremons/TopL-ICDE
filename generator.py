
import random
import copy
import os

import numpy as np
import networkx as nx

from utils.ioutils import create_folder, realworld_raw_data_graph_read


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
    while target_graph.number_of_edges() > node_num * neighbor_num:
        (u, v) = random.sample(target_graph.edges, 1)[0]
        G = copy.deepcopy(target_graph)
        G.remove_edge(u, v)
        if nx.is_connected(G):
            target_graph.remove_edge(u, v)

    # Print infos
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
    for i in target_graph.nodes:
        keyword_num = np.random.randint(max(keywords_per_vertex_num-1, 0), keywords_per_vertex_num+2)  # the num is key_per ± 1
        keywords = random.sample(keywords_set, keyword_num)
        for keyword in keywords:
            label_counter[keyword] += 1
        target_graph.nodes[i]['keywords'] = keywords
        # print(target_graph.nodes[i])

    # print([{keywords_set[i]: label_counter[i]} for i in range(all_keyword_num)])

    # TODO: 2.3. Add the weight (propagation probability) to each edge
    # WC model: pp(u, v) for an edge (u, v) is 1/d(v), where d(v) is the in-degree of v.
    for i in target_graph.nodes:
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


def generate_dataset_based_realworld(seed: int, all_keyword_num: int, keywords_per_vertex_num: int, dataset: str):
    # 0. Read raw dataset from file
    data_graph = realworld_raw_data_graph_read(dataset=dataset)

    # 1. Add the keyword set to each vertex
    keywords_set = range(0, all_keyword_num)
    label_counter = [0 for _ in range(all_keyword_num)]
    for i in data_graph.nodes:
        data_graph.nodes[i].clear()
        keyword_num = np.random.randint(max(keywords_per_vertex_num-1, 0), keywords_per_vertex_num+2)  # the num is key_per ± 1
        keywords = random.sample(keywords_set, keyword_num)
        for keyword in keywords:
            label_counter[keyword] += 1
        data_graph.nodes[i]['keywords'] = keywords
        # print(data_graph.nodes[i])

    # TODO: 2.3. Add the weight (propagation probability) to each edge
    # WC model: pp(u, v) for an edge (u, v) is 1/d(v), where d(v) is the in-degree of v.
    for i in data_graph.nodes:
        neighbors_num = len(list(data_graph.neighbors(i)))
        for neighbor in data_graph.neighbors(i):
            # data_graph.edges[i, neighbor].clear()
            data_graph.edges[i, neighbor]["weight"] = 1 / neighbors_num
            # print(data_graph.get_edge_data(i, neighbor))
    # TRIVALENCY model: randomly select a probability from the set {0.1, 0.01, 0.001}

    # 3. Save the graph as ".gpickle.gz" into a folder, name
    folder_name = os.path.join(
        "dataset",
        "realworld",
        dataset,
        '{0}-{1}-{2}-{3}'.format(
            data_graph.number_of_nodes(),
            data_graph.number_of_edges(),
            all_keyword_num,
            keywords_per_vertex_num
        )
    )
    create_folder(folder_name=folder_name)
    os.chdir(folder_name)  # Switch path to the folder
    nx.write_gpickle(data_graph, 'data_graph.gpickle.gz')
    print(folder_name, 'data_graph.gpickle.gz', "saved successfully!")


if __name__ == "__main__":
    # Set the parameters to generate dataset.
    seed = 2022
    # generate_dataset(
    #     seed=seed,
    #     keywords_per_vertex_num=3,  # 1, 2, 3, 4, 5
    #     all_keyword_num=100,  # 500, 800, 1K, 2K, 5K
    #     node_num=1000,  # 10K, 30K, 50K, 100K, 500K, 1M
    #     neighbor_num=7,
    #     add_edge_probability=0.42
    # )
    # generate_dataset(
    #     seed=seed,
    #     keywords_per_vertex_num=3,  # 1, 2, 3, 4, 5
    #     all_keyword_num=1000,  # 500, 800, 1K, 2K, 5K
    #     node_num=10000,  # 10K, 30K, 50K, 100K, 500K, 1M
    #     neighbor_num=7,
    #     add_edge_probability=0.42
    # )
    # generate_dataset(
    #     seed=seed,
    #     keywords_per_vertex_num=3,  # 1, 2, 3, 4, 5
    #     all_keyword_num=1000,  # 500, 800, 1K, 2K, 5K
    #     node_num=50000,  # 10K, 30K, 50K, 100K, 500K, 1M
    #     neighbor_num=8,
    #     add_edge_probability=0.42
    # )
    # generate_dataset(
    #     seed=seed,
    #     keywords_per_vertex_num=3,  # 1, 2, 3, 4, 5
    #     all_keyword_num=1000,  # 500, 800, 1K, 2K, 5K
    #     node_num=100000,  # 10K, 30K, 50K, 100K, 500K, 1M
    #     neighbor_num=8,
    #     add_edge_probability=0.42
    # )
    # generate_dataset(
    #     seed=seed,
    #     keywords_per_vertex_num=3,  # 1, 2, 3, 4, 5
    #     all_keyword_num=1000,  # 500, 800, 1K, 2K, 5K
    #     node_num=500000,  # 10K, 30K, 50K, 100K, 500K, 1M
    #     neighbor_num=8,
    #     add_edge_probability=0.42
    # )
    # generate_dataset(
    #     seed=seed,
    #     keywords_per_vertex_num=3,  # 1, 2, 3, 4, 5
    #     all_keyword_num=1000,  # 500, 800, 1K, 2K, 5K
    #     node_num=1000000,  # 10K, 30K, 50K, 100K, 500K, 1M
    #     neighbor_num=8,
    #     add_edge_probability=0.42
    # )
    # generate_dataset_based_realworld(
    #     seed=seed,
    #     all_keyword_num=1000,
    #     keywords_per_vertex_num=3,
    #     dataset="dblp"
    # )
    # generate_dataset_based_realworld(
    #     seed=seed,
    #     all_keyword_num=1000,
    #     keywords_per_vertex_num=3,
    #     dataset="amazon"
    # )
    # generate_dataset_based_realworld(
    #     seed=seed,
    #     all_keyword_num=1000,
    #     keywords_per_vertex_num=3,
    #     dataset="epinions"
    # )
    generate_dataset_based_realworld(
        seed=seed,
        all_keyword_num=1000,
        keywords_per_vertex_num=3,
        dataset="facebook"
    )
