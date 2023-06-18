import os
import json
import networkx as nx


def is_precomputed(dataset_path: str) -> bool:
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    mid_graph_file_path = os.path.join(base_path, dataset_path, 'mid_data_graph.gpickle.gz')
    index_json_file_path = os.path.join(base_path, dataset_path, 'index.json')
    return (os.path.exists(mid_graph_file_path) and os.path.exists(index_json_file_path))


# Create folder at "../<folder_name>"
def create_folder(folder_name: str) -> bool:
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    folder_path = os.path.join(base_path, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_name)  # 创建data文件夹
    return True


# Read a data graph folder <dataset_path>
def data_graph_read(dataset_path: str) -> nx.Graph:
    # Load graph from file
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # print("base_path", base_path)
    # print(os.path.join(base_path, dataset_path, 'data_graph.gpickle.gz'))
    data_graph = nx.read_gpickle(os.path.join(base_path, dataset_path, 'data_graph.gpickle.gz'))
    return data_graph


# Read a mid data graph folder <dataset_path>
def mid_graph_read(dataset_path: str) -> (nx.Graph, list):
    # Load graph from file
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # print("base_path", base_path)
    # print(os.path.join(base_path, dataset_path, 'data_graph.gpickle.gz'))
    data_graph = nx.read_gpickle(os.path.join(base_path, dataset_path, 'mid_data_graph.gpickle.gz'))
    return data_graph


# Save the mid graph and index
def mid_graph_save(mid_data_graph: nx.Graph, index: list, dataset_path: str) -> bool:
    create_folder(folder_name=dataset_path)
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    os.chdir(os.path.join(base_path, dataset_path))  # Switch path to the folder
    nx.write_gpickle(mid_data_graph, 'mid_data_graph.gpickle.gz')
    print(dataset_path, 'mid_data_graph.gpickle.gz', "saved successfully!")
    index_json = json.dumps(index)
    json_file = open(os.path.join(dataset_path, 'index.json'), 'w')
    json_file.write(index_json)
    json_file.close()
    print(dataset_path, 'index.json', "saved successfully!")


if __name__ == "__main__":
    dataset_path = os.path.join("dataset", "manual", "50000-124933-1000-3")
    data_graph, index_root = data_graph_read(dataset_path=dataset_path)
