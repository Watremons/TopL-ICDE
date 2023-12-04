import networkx as nx
import os


if __name__ == "__main__":
    data_list = []
    file_path = os.path.join(os.path.dirname(__file__), "com-amazon.ungraph.txt")
    with open(file_path, "r", encoding="utf-8") as f:
        data_list = f.readlines()

    edge_list = []
    for data in data_list:
        if data.startswith("#"):
            continue
        [u, v] = data.strip().split("\t")
        if u != v:
            edge_list.append((int(u), int(v)))
    # print(edge_list)
    data_graph = nx.Graph()
    data_graph.add_edges_from(edge_list)
    print(data_graph)
    os.chdir(os.path.dirname(file_path))
    nx.write_gpickle(data_graph, 'amazon.gpickle.gz')
    print('amazon.gpickle.gz', "saved successfully!")
