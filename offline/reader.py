import os
import networkx as nx


def graph_read(dataset_path: str):
    # Load graph from file
    data_graph = nx.read_gpickle(os.path.join(dataset_path, 'data_graph.gpickle.gz'))
    return data_graph


if __name__ == "__main__":
    dataset_path = os.path.join("dataset", "manual", "50000-124933-1000-3")
    data_graph = graph_read(dataset_path=dataset_path)
