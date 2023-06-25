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
    seen = set()
    for node_u in return_graph.nodes:
        u_neighbors_set = set(return_graph.neighbors(node_u))
        seen.add(node_u)
        u_neighbors_filtered = [v for v in u_neighbors_set if v not in seen]
        for node_v in u_neighbors_filtered:
            return_graph.edges[node_u, node_v]["ub_sup"] = len(u_neighbors_set & set(return_graph.neighbors(node_v)))
    return return_graph


# Compute the maximum support value in graph
def compute_k_truss(graph: nx.Graph, k: int) -> nx.Graph:
    temp_graph = graph.copy()
    # key: old graph, value: new graph
    vertex_index_mapping = dict(zip([node for node in temp_graph.nodes()], [i for i in range(temp_graph.number_of_nodes())]))
    node_info_list = [(node_info[0], node_info[1]['N'].copy()) for node_info in temp_graph.nodes(data=True)]
    n_dropped = -1
    to_drop = []
    while n_dropped < len(to_drop):  # if equal, no edge is deleted
        n_dropped = len(to_drop)
        seen = set()
        # traverse the graph
        for u in node_info_list:
            u_neighbors = u[1]
            # print(u_neighbors)
            seen.add(u[0])
            # save the neighbors not seen
            new_u_neighbors = [v for v in u_neighbors if (v not in seen and temp_graph.has_node(v))]
            if len(new_u_neighbors) == 0:
                continue
            v_neighbors_list = [node_info_list[vertex_index_mapping[v]][1] for v in new_u_neighbors]
            index_for_v_neighbors_list = [0 for _ in new_u_neighbors]  # Save a index for each u_neighbor
            support_for_v_neighbors_list = [0 for _ in new_u_neighbors]  # Save a index for each u_neighbor
            index_for_u_neighbors = 0
            while True:  # Sort merge join
                now_vertex_in_u_neighbors = new_u_neighbors[index_for_u_neighbors]
                for idx, v in enumerate(new_u_neighbors):
                    if index_for_v_neighbors_list[idx] == len(v_neighbors_list[idx]):
                        continue
                    now_vertex_in_v_neighbors = v_neighbors_list[idx][index_for_v_neighbors_list[idx]]
                    while now_vertex_in_u_neighbors >= now_vertex_in_v_neighbors:
                        if now_vertex_in_u_neighbors == now_vertex_in_v_neighbors:  # if equaling, counter += 1
                            support_for_v_neighbors_list[idx] += 1
                        index_for_v_neighbors_list[idx] += 1  # Move to next neighbor in v_neighbors
                        if index_for_v_neighbors_list[idx] == len(v_neighbors_list[idx]):
                            break
                        now_vertex_in_v_neighbors = v_neighbors_list[idx][index_for_v_neighbors_list[idx]]
                if all(index_for_v_neighbors_list[idx] == len(v_neighbors_list[idx]) for idx in range(len(new_u_neighbors))):  # All of v_neighbors is visited
                    break
                index_for_u_neighbors += 1
                if index_for_u_neighbors == len(new_u_neighbors):  # All of u_neighbors is visited
                    break
            for v_idx, support_for_v_neighbors in enumerate(support_for_v_neighbors_list):
                # print(support_for_v_neighbors)
                if support_for_v_neighbors < (k - 2):  # if the triangle
                    node_info_list[vertex_index_mapping[u[0]]][1].remove(new_u_neighbors[v_idx])
                    node_info_list[vertex_index_mapping[new_u_neighbors[v_idx]]][1].remove(u[0])
                    to_drop.append((u[0], new_u_neighbors[v_idx]))
    temp_graph.remove_edges_from(to_drop)
    temp_graph.remove_nodes_from(list(nx.isolates(temp_graph)))
    return temp_graph


# Compute the maximum support value in graph
# def compute_k_truss(graph: nx.Graph, k: int) -> nx.Graph:
#     temp_graph = graph.copy()

#     n_dropped = 1
#     while n_dropped > 0:
#         n_dropped = 0
#         to_drop = []
#         seen = set()
#         for u in temp_graph:
#             nbrs_u = set(temp_graph.neighbors(u))
#             seen.add(u)
#             new_nbrs = [v for v in nbrs_u if v not in seen]
#             for v in new_nbrs:
#                 if len(nbrs_u & set(temp_graph.neighbors(v))) < (k - 2):
#                     to_drop.append((u, v))
#         temp_graph.remove_edges_from(to_drop)
#         n_dropped = len(to_drop)
#         temp_graph.remove_nodes_from(list(nx.isolates(temp_graph)))

#     return temp_graph


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
                        heapq.heappush(to_traverse, ((-1)*data_graph.edges[node, node_neighbor]['weight'], node_neighbor))
                        flag = True
                        break
                if not flag and data_graph.edges[node, node_neighbor]['weight'] > threshold:
                    heapq.heappush(to_traverse, ((-1)*data_graph.edges[node, node_neighbor]['weight'], node_neighbor))
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
