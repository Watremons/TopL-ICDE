import os
import random
import numpy as np
import networkx as nx
from scipy.stats import zipf


def replace_keywords(dataset: str, distribution: str):
    # Set seed
    seed = 2022
    random.seed(seed)
    np.random.seed(seed)

    # Set path
    [node_num, edge_num, all_keywords_num, per_vertex_keyword] = dataset.split("-")
    node_num = int(node_num)
    edge_num = int(edge_num)
    all_keywords_num = int(all_keywords_num)
    per_vertex_keyword = int(per_vertex_keyword)
    base_path = os.path.abspath(os.path.dirname(__file__))
    input_file_path = os.path.join(base_path, "dataset", "manual", dataset, 'data_graph.gpickle.gz')
    # Load graph
    target_graph = nx.read_gpickle(input_file_path)
    if distribution == "zipf":
        # Zipf
        a = 2  # param
        zipf_dist = zipf(a)
        size = target_graph.number_of_nodes()
        keywords_set = zipf_dist.rvs(size * per_vertex_keyword)
    elif distribution == "gauss":
        # Gaussian
        mean = 500  # 均值
        stddev = 150  # 标准差
        if all_keywords_num == 100:
            mean = 50  # 均值
            stddev = 15  # 标准差
        elif all_keywords_num == 500:
            mean = 250  # 均值
            stddev = 75  # 标准差
        elif all_keywords_num == 800:
            mean = 400  # 均值
            stddev = 120  # 标准差
        elif all_keywords_num == 1000:
            mean = 500  # 均值
            stddev = 150  # 标准差
        elif all_keywords_num == 2000:
            mean = 1000  # 均值
            stddev = 300  # 标准差
        elif all_keywords_num == 5000:
            mean = 2500  # 均值
            stddev = 750  # 标准差
        size = target_graph.number_of_nodes()
        keywords_set = np.random.normal(mean, stddev, size)
    keywords_set = np.clip(keywords_set, 0, all_keywords_num-1).astype(int)

    label_counter = [0 for _ in range(all_keywords_num)]
    for i, node in enumerate(target_graph):
        keyword_num = np.random.randint(max(per_vertex_keyword-1, 0), per_vertex_keyword+2)  # the num is key_per ± 1

        keywords = np.random.choice(keywords_set, keyword_num)
        while len(set(keywords)) != len(keywords):
            keywords = np.random.choice(keywords_set, keyword_num)
        for keyword in keywords:
            label_counter[keyword] += 1
        target_graph.nodes[node]['name'] = keywords

    print(max(keywords_set))
    print(min(keywords_set))
    print(label_counter)
    output_file_path = os.path.join(base_path, "dataset", "manual", dataset, distribution, 'data_graph.gpickle.gz')
    if not os.path.exists(os.path.dirname(output_file_path)):
        os.makedirs(os.path.dirname(output_file_path))  # 创建data文件夹

    # Save graph
    nx.write_gpickle(target_graph, output_file_path)


if __name__ == "__main__":
    # dataset = "1000-2473-100-3"
    # dataset = "10000-24999-1000-3"
    # dataset = "30000-74907-1000-3"
    # dataset = "50000-124933-500-5"
    # dataset = "50000-124933-800-5"
    # dataset = "50000-124933-1000-1"
    # dataset = "50000-124933-1000-2"
    dataset = "50000-124933-1000-3"
    # dataset = "50000-124933-1000-4"
    # dataset = "50000-124933-1000-5"
    # dataset = "50000-124933-2000-3"
    # dataset = "50000-124933-5000-3"
    # dataset = "100000-249940-1000-3"
    # dataset = "500000-1249915-1000-3"
    # dataset = "1000000-2500002-1000-3"
    replace_keywords(
        dataset=dataset,
        distribution="gauss"
    )
    replace_keywords(
        dataset=dataset,
        distribution="zipf"
    )
