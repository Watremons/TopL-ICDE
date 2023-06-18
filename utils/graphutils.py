import heapq
import networkx as nx


# Compute hop(v,r)
def compute_hop_v_r(graph: nx.Graph, node_v: int, radius: int) -> nx.Graph:
    nodes_in_hop = []
    to_traverse = [node_v]
    for r_dev in range(radius):
        new_to_traverse = []
        for node in to_traverse:
            for neighbor in graph.neighbors(node):
                if neighbor not in nodes_in_hop:
                    nodes_in_hop.append(neighbor)
                    new_to_traverse.append(neighbor)
        to_traverse = new_to_traverse
    return graph.subgraph(nodes_in_hop)


# Compute maximum support in graph
def compute_support(graph: nx.Graph) -> nx.Graph:
    return_graph = graph.copy()
    for node_u in return_graph.nodes:
        for node_v in return_graph.neighbors(node_u):
            if node_u > node_v:  # Make sure compute only once
                return_graph.edges[node_u, node_v]["ub_sup"] = len(list(nx.common_neighbors(return_graph, node_u, node_v)))  # The support value equals to the common neighbor number
    return return_graph


# Compute the maximum support value in graph
def compute_k_truss(graph: nx.Graph, k: int) -> nx.Graph:
    if nx.number_of_selfloops(graph) > 0:
        msg = (
            "Input graph has self loops which is not permitted; "
            "Consider using G.remove_edges_from(nx.selfloop_edges(G))."
        )
        raise IndexError(msg)

    temp_graph = graph.copy()

    n_dropped = 1
    while n_dropped > 0:
        n_dropped = 0
        to_drop = []
        seen = set()
        for u in temp_graph:
            nbrs_u = set(temp_graph[u])
            seen.add(u)
            new_nbrs = [v for v in nbrs_u if v not in seen]
            for v in new_nbrs:
                if len(nbrs_u & set(temp_graph[v])) < (k - 2):
                    to_drop.append((u, v))
        temp_graph.remove_edges_from(to_drop)
        n_dropped = len(to_drop)
        temp_graph.remove_nodes_from(list(nx.isolates(temp_graph)))

    return temp_graph


# Compute the influential score
def compute_influential_score(seed_community: nx.Graph, data_graph: nx.Graph, threshold: float) -> float:
    # 0. obtain the nodes used in first turn
    propagation_probability_dict = dict()  # save the distance at each moment
    to_traverse = []  # save the to do vertices next turn (distance, node_index)
    for node in seed_community.nodes:
        for node_neighbor in data_graph.neighbors(node):
            if node_neighbor not in seed_community.nodes:  # pick the vertices who is in 1-hop of vertices in seed community
                flag = False
                # if it appeared in f
                for (score, idx) in to_traverse:
                    if idx == node_neighbor and ((-1)*score) < data_graph.edges[node, node_neighbor]['weight']:
                        to_traverse.remove((score, node_neighbor))
                        to_traverse.append(((-1)*data_graph.edges[node, node_neighbor]['weight'], node_neighbor))
                        flag = True
                        break
                if not flag and data_graph.edges[node, node_neighbor]['weight'] > threshold:
                    to_traverse.append(((-1)*data_graph.edges[node, node_neighbor]['weight'], node_neighbor))
    heapq.heapify(to_traverse)  # keep a maximum heap
    # print("to_traverse", to_traverse)
    # 1. do dijkstra until there is no edge to go
    while len(to_traverse) > 0:
        # 1.1. pop the to_do_node with greatest weight
        (max_propagation_probability, node_index) = heapq.heappop(to_traverse)
        max_propagation_probability = (-1)*max_propagation_probability
        # 1.2. add the node into dict
        propagation_probability_dict[node_index] = max_propagation_probability
        # 1.3. update the max score of its neighbors
        for node_neighbor in data_graph.neighbors(node_index):
            if node_neighbor not in propagation_probability_dict and node_neighbor not in seed_community.nodes:  # neighbor is unvisited
                new_dis_to_neighbor = propagation_probability_dict[node_index] * data_graph.edges[node_index, node_neighbor]['weight']
                node_neighbor_score = threshold
                for (score, idx) in to_traverse:
                    if idx == node_neighbor:
                        node_neighbor_score = -1*score
                if new_dis_to_neighbor > node_neighbor_score:
                    if node_neighbor_score != threshold:
                        to_traverse.remove((-1*node_neighbor_score, node_neighbor))
                    to_traverse.append((-1*new_dis_to_neighbor, node_neighbor))
        heapq.heapify(to_traverse)
    # print(seed_community.nodes)
    # print(data_graph.edges)
    # print(propagation_probability_dict)
    influential_score = 0
    for (node_index, propagation_probability) in propagation_probability_dict.items():
        influential_score = influential_score + propagation_probability
    # print("influential_score", influential_score)
    return influential_score
