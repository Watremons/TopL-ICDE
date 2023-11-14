import heapq
import time
from itertools import combinations
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


def update_diversity_score_for_graph(data_graph: nx.Graph, influenced_community: nx.Graph):
    for influenced_node in influenced_community.nodes(data=True):
        if "max_influential_score" not in data_graph.nodes[influenced_node[0]] or data_graph.nodes[influenced_node[0]]["max_influential_score"] < influenced_node[1]["influential_score"]:
            data_graph.nodes[influenced_node[0]]["max_influential_score"] = influenced_node[1]["influential_score"]
    return data_graph


class IncrementEntry:
    def __init__(self, key_increment: float, entity_subgraph: nx.Graph, influenced_community: nx.Graph):
        self.key_increment = key_increment
        self.entity_subgraph = entity_subgraph
        self.influenced_community = influenced_community

    def __lt__(self, other):
        return self.key_increment < other.key_increment


def execute_refine_without_pruning(
    query_L: int,
    data_graph: nx.Graph,
    input_set: set,
    stat: Statistics
) -> (set, int):
    # 0.1. initialize the max heap
    max_increment_entry_heap = []
    for candidate in input_set:
        heapq.heappush(
            max_increment_entry_heap, IncrementEntry(
                key_increment=-1*candidate[1],
                entity_subgraph=candidate[0],
                influenced_community=candidate[2],
            )
        )
    # 0.2. initialize the round count and result set
    result_set = set()
    total_diversity_score = 0
    start_timestamp = time.time()
    temp_data_graph = data_graph.copy(as_view=False)
    stat.refinement_grah_copy_time += (time.time() - start_timestamp)
    while len(result_set) < query_L and len(max_increment_entry_heap) > 0:
        start_timestamp = time.time()
        # 1.1. get the maximum one
        now_increment_entry = heapq.heappop(max_increment_entry_heap)
        stat.select_greatest_increment_entry_time += (time.time() - start_timestamp)
        # 1.2. add the one to result set
        total_diversity_score += -1*now_increment_entry.key_increment
        result_set.add((now_increment_entry.entity_subgraph, -1*now_increment_entry.key_increment, now_increment_entry.influenced_community))  # (seed_community_g, diversity_g)

        start_timestamp = time.time()
        temp_data_graph = update_diversity_score_for_graph(
            data_graph=temp_data_graph,
            influenced_community=now_increment_entry.influenced_community
        )
        stat.refinement_graph_update_time += (time.time() - start_timestamp)
        # 1.3. update the increment of candidate
        for idx, now_increment_entry in enumerate(max_increment_entry_heap):
            start_timestamp = time.time()
            delta_diversity_score = compute_diversity_score_increment(
                data_graph=temp_data_graph,
                influenced_community_g_inf=now_increment_entry.influenced_community,
            )
            stat.refinement_increment_compute_time += (time.time() - start_timestamp)
            stat.refinement_increment_compute_counter += 1
            max_increment_entry_heap[idx].key_increment = -1*delta_diversity_score
        # 1.4. resort the heap
        heapq.heapify(max_increment_entry_heap)
    return result_set, total_diversity_score


def execute_refine_optimal(
    query_L: int,
    data_graph: nx.Graph,
    input_set: set,
    stat: Statistics
) -> (set, int):
    # 0. generate all possible combinations
    possible_combinations = [c for c in combinations(input_set, query_L)]

    # total_start_timestamp = time.time()
    # total_time = 0

    result_set = set()
    max_diversity_score = 0
    # 1. iterate the possible combinations
    for idx, possible_result_set in enumerate(possible_combinations):
        # if (idx+1) % 1000 == 0:
        #     print("Optimal result compuing", idx+1, "in", len(possible_combinations))

        if idx == 253:  # Total combination: 53130 = 253 * 210
            print("Optimal result compuing for", idx, " as estimation\n")
            break
        # 1.1. iterate the possible combinations
        # one_turn_start_timestamp = time.time()

        now_diversity_score = 0
        now_result_set = set()
        start_timestamp = time.time()
        temp_data_graph = data_graph.copy(as_view=False)
        stat.refinement_grah_copy_time += (time.time() - start_timestamp)
        # 1.2. iterate the seed community in each combination
        for (seed_community, _, influenced_community_g_inf) in possible_result_set:
            start_timestamp = time.time()
            # 1.2.1 compute the delta diversity score for this influenced community
            delta_diversity_score = compute_diversity_score_increment(
                data_graph=temp_data_graph,
                influenced_community_g_inf=influenced_community_g_inf,
            )
            stat.refinement_increment_compute_time += (time.time() - start_timestamp)
            # print("increment_compute Time: ", (time.time() - start_timestamp))
            stat.refinement_increment_compute_counter += 1
            # 1.2.2 update the diversity score for graph
            start_timestamp = time.time()
            temp_data_graph = update_diversity_score_for_graph(
                data_graph=temp_data_graph,
                influenced_community=influenced_community_g_inf
            )
            # 1.2.3 accumulate the diversity score
            now_diversity_score += delta_diversity_score
            stat.refinement_graph_update_time += (time.time() - start_timestamp)
            # print("graph_update Time: ", (time.time() - start_timestamp))

            now_result_set.add((seed_community, delta_diversity_score, influenced_community_g_inf))
        if now_diversity_score > max_diversity_score:
            result_set = now_result_set
            max_diversity_score = now_diversity_score
        # print("One turn Time: ", idx, (time.time() - one_turn_start_timestamp))
        # total_time += (time.time() - one_turn_start_timestamp)
        # print("Total Time:", total_time)

    # print("Refine Time", time.time() - total_start_timestamp)
    # Total combination: 53130 = 253 * 210
    # make estimation
    # print("compute time:", stat.refinement_increment_compute_time, "for", stat.refinement_increment_compute_counter)
    stat.optimal_sampling_ratio = 210

    return result_set, max_diversity_score
