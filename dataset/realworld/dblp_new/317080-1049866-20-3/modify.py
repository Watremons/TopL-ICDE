import os
import numpy as np
import random

import networkx as nx

R_MAX = 2

if __name__ == "__main__":
    base_path = os.path.abspath(os.path.dirname(__file__))
    data_graph = nx.read_gpickle(os.path.join(base_path, 'mid_data_graph.gpickle.gz'))
    all_keyword_num = 20
    keywords_per_vertex_num = 3
    # 0. save the neighbors in vertex
    for i in data_graph.nodes:
        data_graph.nodes[i]["N"] = list(data_graph.neighbors(i))
    print("neighbors N for each vertex is computed")

    # 1. Add the keyword set to each vertex
    keywords_set = range(0, all_keyword_num)
    label_counter = [0 for _ in range(all_keyword_num)]
    for i in data_graph.nodes:
        keyword_num = np.random.randint(max(keywords_per_vertex_num-1, 1), keywords_per_vertex_num+2)  # the num is key_per ± 1
        keywords = random.sample(keywords_set, keyword_num)
        for keyword in keywords:
            label_counter[keyword] += 1
        data_graph.nodes[i]['keywords'] = keywords

    for node_index, i in enumerate(data_graph.nodes):
        if (node_index+1) % 100 == 0:
            print("BV and ub_sup for node", node_index+1, "in", data_graph.number_of_nodes(), "has neighbors", len(list(data_graph.neighbors(i))))
        bv = 0
        # 1.1 hash keywords to BV for each vertex
        for keyword in data_graph.nodes[node_index]["keywords"]:
            bv = bv | (1 << keyword)
        # 1.2 save BV into R
        data_graph.nodes[node_index]["BV"] = bv
        # print("End to save BV as integer")

    # 3. compute r-hop and R for each r in [1, r_max] and each vertex
    for node_index, i in enumerate(data_graph.nodes):
        if (node_index+1) % 100 == 0:
            print("BV_r, ub_sup_r and Inf_ub for node", node_index+1, "in", data_graph.number_of_nodes())
        for r in range(R_MAX):  # [1, r_max]
            # 3.0. compute hop(v_i, r)
            # starttime = time.time()
            hop_v_r = nx.ego_graph(G=data_graph, n=node_index, radius=r+1, center=True)
            # print("compute r-hop", time.time()-starttime)
            # hop_v_r = compute_hop_v_r(graph=data_graph, node_v=i, radius=r+1)
            # 3.1. compute bv_r = all BV on vertices in hop(v_i, r)
            # starttime = time.time()
            for node_j in hop_v_r.nodes:  # int bit-or int
                data_graph.nodes[node_index]["R"][r]["BV_r"] = data_graph.nodes[node_index]["R"][r]["BV_r"] | hop_v_r.nodes[node_j]["BV"]
            # print("compute BV_r", time.time()-starttime)
    base_path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(base_path)  # Switch path to the folder
    nx.write_gpickle(data_graph, 'new_mid_data_graph.gpickle.gz')