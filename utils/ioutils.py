import os
import json
import time
import networkx as nx
import numpy as np


class JsonEncoder(json.JSONEncoder):
    """Convert numpy classes to JSON serializable objects."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()


def is_precomputed(dataset_path: str) -> bool:
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    mid_graph_file_path = os.path.join(base_path, dataset_path, 'mid_data_graph.gpickle.gz')
    return os.path.exists(mid_graph_file_path)


def is_indexed(dataset_path: str) -> bool:
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    index_json_file_path = os.path.join(base_path, dataset_path, 'index.json')
    return os.path.exists(index_json_file_path)


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


# Read a raw data graph
def realworld_raw_data_graph_read(dataset: str) -> nx.Graph:
    # Load graph from file
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    file_path = os.path.join(base_path, "dataset", "realworld", dataset, dataset + '.gpickle.gz')
    # print("base_path", base_path)
    # print(os.path.join(base_path, dataset_path, 'data_graph.gpickle.gz'))
    data_graph = nx.read_gpickle(file_path)
    return data_graph


# Read a mid data graph from folder <dataset_path>
def mid_graph_read(dataset_path: str) -> nx.Graph:
    # Load graph from file
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # print("base_path", base_path)
    # print(os.path.join(base_path, dataset_path, 'data_graph.gpickle.gz'))
    data_graph = nx.read_gpickle(os.path.join(base_path, dataset_path, 'mid_data_graph.gpickle.gz'))
    print(dataset_path, 'mid_data_graph.gpickle.gz', "loaded successfully!")
    return data_graph


# Read a index from folder <dataset_path>
def index_read(dataset_path: str) -> list:
    # Load graph from file
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    json_file = open(os.path.join(base_path, dataset_path, 'index.json'), 'r')
    json_content = json_file.read()
    json_file.close()
    index_json = json.loads(json_content)
    print(dataset_path, 'index.json', "loaded successfully!")
    return index_json


# Save the precomputed graph
def mid_graph_save(mid_data_graph: nx.Graph, dataset_path: str) -> bool:
    create_folder(folder_name=dataset_path)
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    os.chdir(os.path.join(base_path, dataset_path))  # Switch path to the folder
    nx.write_gpickle(mid_data_graph, 'mid_data_graph.gpickle.gz')
    print(dataset_path, 'mid_data_graph.gpickle.gz', "saved successfully!")
    return True


# Save the index
def index_save(index: list, dataset_path: str) -> bool:
    create_folder(folder_name=dataset_path)
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # print(index)
    index_json = json.dumps(index, cls=JsonEncoder)
    json_file = open(os.path.join(base_path, dataset_path, 'index.json'), 'w')
    json_file.write(index_json)
    json_file.close()
    print(dataset_path, 'index.json', "saved successfully!")
    return True


# Save the result graphs
def result_graph_save(result_graph: list, dataset_path: str) -> bool:
    create_folder(folder_name=dataset_path)
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    os.chdir(os.path.join(base_path, dataset_path))  # Switch path to the folder
    nx.write_gpickle(result_graph, 'result_graph_list.gpickle.gz')
    return True


# Save the result statistics
def statistic_file_save(stat, dataset_path: str) -> bool:
    create_folder(folder_name=dataset_path)
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    stat_file = 'statistics-' + time.strftime('%m%d-%H%M%S', time.localtime()) + "-" + str(time.time()) + '.txt'
    result_stat_file = open(os.path.join(base_path, dataset_path, stat_file), 'w')
    result_stat_file.write(stat.generate_stat_result())
    result_stat_file.close()
    print(stat.output_stat_file_name, "saved successfully!")
    return True


def read_graph_simple(graph_path: str) -> nx.Graph:
    data_graph = nx.read_gpickle(graph_path)
    return data_graph


if __name__ == "__main__":
    data_graph_list = read_graph_simple(graph_path=os.path.join(os.path.dirname(__file__), "result_graph0.gpickle.gz"))
    BV_list = []
    for graph in data_graph_list:
        print(graph)
        bv_g = set()
        for node in graph.nodes(data=True):
            print(node[0], node[1]["keywords"])
            # print(node[0], bin(node[1]["BV"]))
