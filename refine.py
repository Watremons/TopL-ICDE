import heapq
import time
import math
import networkx as nx

from online.statistics import Statistics


def compute_diversity_score_increment(data_graph: nx.Graph, influenced_community_g_inf: nx.Graph) -> float:
    # 1. initialization
    delta_diversity_score = 0
    for influenced_node in influenced_community_g_inf.nodes(data=True):
        # 2. get the raw influential score in the data graph
        raw_influential_score = 0
        if "max_influential_score" in data_graph.nodes[influenced_node[0]]:
            raw_influential_score = data_graph.nodes[influenced_node[0]]["max_influential_score"]
        # 3. update the max influential score for the node and accumlate the total increment
        if raw_influential_score < influenced_node[1]["influential_score"]:
            delta_diversity_score += (influenced_node[1]["influential_score"] - raw_influential_score)
    return delta_diversity_score


def compute_diversity_score(data_graph: nx.Graph, influenced_community: nx.Graph):
    for influenced_node in influenced_community.nodes(data=True):
        if "max_influential_score" not in data_graph.nodes[influenced_node[0]] or data_graph.nodes[influenced_node[0]]["max_influential_score"] < influenced_node[1]["influential_score"]:
            data_graph.nodes[influenced_node[0]]["max_influential_score"] = influenced_node[1]["influential_score"]
    return data_graph


class IncrementEntry:
    def __init__(self, key_increment: float, entity_subgraph: nx.Graph, influenced_community: nx.Graph, rounds: int):
        self.key_increment = key_increment
        self.entity_subgraph = entity_subgraph
        self.influenced_community = influenced_community
        self.rounds = rounds

    def __lt__(self, other):
        if math.fabs(self.key_increment - other.key_increment) < 0.0001:
            return self.rounds < self.rounds
        else:
            return self.key_increment < other.key_increment


def execute_refine(
    query_L: int,
    data_graph: nx.Graph,
    input_set: set,
    stat: Statistics
) -> list:
    # 0.1. initialize the max heap
    max_increment_entry_heap = []
    for candidate in input_set:
        heapq.heappush(
            max_increment_entry_heap, IncrementEntry(
                key_increment=-1*candidate[1],
                entity_subgraph=candidate[0],
                influenced_community=candidate[2],
                rounds=0
            )
        )
    # 0.2. initialize the round count and result set
    result_set = set()
    round_count = 0
    temp_data_graph = data_graph.copy(as_view=False)
    while len(result_set) < query_L and len(max_increment_entry_heap) > 0:
        for increment_entry in max_increment_entry_heap:
            print(increment_entry.key_increment, increment_entry.entity_subgraph, "[{}]".format(increment_entry.rounds))
        print("\n")

        start_timestamp = time.time()
        now_increment_entry = heapq.heappop(max_increment_entry_heap)
        stat.select_greatest_increment_entry_time += (time.time() - start_timestamp)
        if now_increment_entry.rounds == round_count:
            result_set.add((now_increment_entry.entity_subgraph, -1*now_increment_entry.key_increment, now_increment_entry.influenced_community))  # (seed_community_g, diversity_g)
            temp_data_graph = compute_diversity_score(
                data_graph=temp_data_graph,
                influenced_community=now_increment_entry.influenced_community
            )
            round_count += 1
        else:
            start_timestamp = time.time()
            delta_diversity_score = compute_diversity_score_increment(
                data_graph=temp_data_graph,
                influenced_community_g_inf=now_increment_entry.influenced_community,
            )
            stat.refinement_increment_compute_time += (time.time() - start_timestamp)
            stat.refinement_increment_compute_count += 1
            heapq.heappush(
                max_increment_entry_heap,
                IncrementEntry(
                    key_increment=-1*delta_diversity_score,
                    entity_subgraph=now_increment_entry.entity_subgraph,
                    influenced_community=now_increment_entry.influenced_community,
                    rounds=round_count
                )
            )

    return result_set
