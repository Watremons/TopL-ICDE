import os
import random
import numpy as np
import networkx as nx


R_MAX = 2


def dict_add(to_do_dict: dict, add_key: int, add_value: tuple):
    if add_key not in to_do_dict:
        to_do_dict[add_key] = [add_value]
    else:
        to_do_dict[add_key].append(add_value)


def sort_edges_by_ub_sup(graph: nx.Graph) -> dict:
    edge_dict = dict()
    for edge in graph.edges.data():
        now_edge_tuple = (edge[0], edge[1])
        now_ub_sup = edge[2]['ub_sup']
        dict_add(to_do_dict=edge_dict, add_key=now_ub_sup, add_value=now_edge_tuple)
    return edge_dict


def truss_decompose(graph: nx.Graph) -> nx.Graph:
    temp_graph = graph.copy()
    # 0: set the init k
    k = 3
    # 1: gather the edge by ub_sup
    edge_dict = sort_edges_by_ub_sup(graph=graph)
    # if there exists edge with support smaller than k-2 (means equal to k-3)
    while len(edge_dict[k-3]) > 0:
        print("Start to process {0} edges with sup {1}".format(len(edge_dict[k-3]), k-3))
        print([(key, len(edge_dict[key])) for key in edge_dict.keys()])

        count = 1
        for discard_edge in edge_dict[k-3]:
            # compute the common neighbors (cn)
            u = discard_edge[0]
            v = discard_edge[1]
            common_neighbors_set = list(set(temp_graph.neighbors(u)) & set(temp_graph.neighbors(v)))
            # print("u_v", (u, v, len(common_neighbors_set)))
            # move the edges (from u or v to cn) to ub_sup-1
            for cn in common_neighbors_set:
                ub_sup_u_cn = temp_graph.edges[u, cn]['ub_sup']
                # print("u_cn", (u, cn, ub_sup_u_cn))
                if (u, cn) in edge_dict[ub_sup_u_cn]:
                    edge_dict[ub_sup_u_cn].remove((u, cn))
                else:
                    edge_dict[ub_sup_u_cn].remove((cn, u))
                # if ub_sup_u_cn-1 < k-3
                if ub_sup_u_cn < k-2:
                    temp_graph.remove_edge(u, cn)
                    graph.edges[u, cn]['ub_sup'] = k-1
                else:
                    dict_add(to_do_dict=edge_dict, add_key=ub_sup_u_cn-1, add_value=(u, cn))
                    temp_graph.edges[u, cn]['ub_sup'] = ub_sup_u_cn-1

                ub_sup_v_cn = temp_graph.edges[v, cn]['ub_sup']
                # print("v_cn", (v, cn, ub_sup_v_cn))
                if (v, cn) in edge_dict[ub_sup_v_cn]:
                    edge_dict[ub_sup_v_cn].remove((v, cn))
                else:
                    edge_dict[ub_sup_v_cn].remove((cn, v))
                # if ub_sup_v_cn-1 < k-3
                if ub_sup_v_cn < k-2:
                    temp_graph.remove_edge(v, cn)
                    graph.edges[v, cn]['ub_sup'] = k-1
                else:
                    dict_add(to_do_dict=edge_dict, add_key=ub_sup_v_cn-1, add_value=(v, cn))
                    temp_graph.edges[v, cn]['ub_sup'] = ub_sup_v_cn-1
            if count % 10000 == 0:
                print("Processed {0} edges".format(count))
            count = count + 1

        # clear the array of now support
        print("Finished processing {0} edges with sup {1}".format(len(edge_dict[k-3]), k-3))
        print([(key, len(edge_dict[key])) for key in edge_dict.keys()])
        for discard_edge in edge_dict[k-3]:
            u = discard_edge[0]
            v = discard_edge[1]
            # record the trussness of (u,v) as k-1
            temp_graph.remove_edge(u, v)
            graph.edges[u, v]['ub_sup'] = k-1
        edge_dict[k-3].clear()
        k = k + 1


def recompute_ub_sup_r_in_synopsis(node_index: int, data_graph: nx.Graph):
    for r in range(R_MAX):  # [1, r_max]
        # 3.0. compute hop(v_i, r)
        hop_v_r = nx.ego_graph(G=data_graph, n=node_index, radius=r+1, center=True)
        # 3.2. compute ub_sup_r = max support of all edges in hop(v_i, r)
        for (u, v) in hop_v_r.edges:
            if u > v and hop_v_r.edges[u, v]["ub_sup"] > data_graph.nodes[node_index]["R"][r]["ub_sup_r"]:
                data_graph.nodes[node_index]["R"][r]["ub_sup_r"] = hop_v_r.edges[u, v]["ub_sup"]


def replace_ub_sup(dataset: str):
    # Set seed
    seed = 2024
    random.seed(seed)
    np.random.seed(seed)

    # Set path
    base_path = os.path.abspath(os.path.dirname(__file__))
    input_file_path = os.path.join(base_path, "dataset_atindex", dataset, 'mid_data_graph.gpickle.gz')
    # Load graph
    target_graph = nx.read_gpickle(input_file_path)
    edge_dict = sort_edges_by_ub_sup(graph=target_graph)
    print([(key, len(edge_dict[key])) for key in edge_dict.keys()])

    truss_decompose(target_graph)
    edge_dict = sort_edges_by_ub_sup(graph=target_graph)
    print([(key, len(edge_dict[key])) for key in edge_dict.keys()])

    # 3. compute r-hop and R for each r in [1, r_max] and each vertex
    for node_index, i in enumerate(target_graph.nodes):
        if (node_index+1) % 100 == 0:
            print("ub_sup_r for node", node_index+1, "in", target_graph.number_of_nodes())
        recompute_ub_sup_r_in_synopsis(node_index=i, data_graph=target_graph)

    print("Synopsis for each vertex is computed")
    # Save the mid graph
    dataset_path = os.path.join(base_path, "dataset_atindex", dataset)
    os.chdir(dataset_path)  # Switch path to the folder
    nx.write_gpickle(target_graph, 'mid_data_graph.gpickle.gz')
    print(dataset_path, 'mid_data_graph.gpickle.gz', "saved successfully!")


if __name__ == "__main__":
    # dataset = "50000-145648-20-3"
    # replace_ub_sup(
    #     dataset=os.path.join("manual", dataset)
    # )

    # dataset = os.path.join("50000-145648-20-3", "gauss")
    # replace_ub_sup(
    #     dataset=os.path.join("manual", dataset)
    # )

    # dataset = os.path.join("50000-145648-20-3", "zipf")
    # replace_ub_sup(
    #     dataset=os.path.join("manual", dataset)
    # )

    dataset = os.path.join("amazon", "334863-925872-20-3")
    replace_ub_sup(
        dataset=os.path.join("realworld", dataset)
    )

    # dataset = os.path.join("dblp_simple", "317080-1049866-1000-3")
    # replace_ub_sup(
    #     dataset=os.path.join("realworld", dataset)
    # )
