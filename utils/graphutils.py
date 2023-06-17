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
