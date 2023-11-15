import time

from utils.argparser import args_parser
from utils.ioutils import data_graph_read, mid_graph_save, index_save, mid_graph_read, index_read, is_precomputed, is_indexed, result_graph_save, statistic_file_save
from online.statistics import Statistics
from precompute import execute_offline, construct_index
from process import execute_online
from refine import execute_refine
from refine_baseline import execute_refine_optimal, execute_refine_without_pruning


def count_leaf_node(now_index):
    if len(now_index) == 0:
        return 0
    if now_index[0]["T"]:
        return 1
    now_counter = 0
    for next_index_entry in now_index:
        now_counter += count_leaf_node(next_index_entry["P"])
    return now_counter


if __name__ == "__main__":
    args = args_parser()
    stat = Statistics(
        input_file_folder=args.input,
        query_keyword_Q=[int(keyword) for keyword in args.keywords.split(",")],
        query_support_k=args.support,
        radius_r=args.radius,
        threshold_theta=args.theta,
        query_L=args.top,
        diversity=args.diversity,
        nlparam=args.nlparam,
        optimal=args.optimal,
        naive=args.naive
    )
    # 1. pre-computation
    if not is_precomputed(args.input):
        print("\nNo available precomputed graph!")
        print("Start offline pre-computation:")
        # 1.1. read data graph
        data_graph = data_graph_read(args.input)
        precompute_start_timestamp = time.time()
        # 1.2. execute offline compute
        mid_data_graph = execute_offline(data_graph=data_graph)
        print("Precompute time:", (time.time() - precompute_start_timestamp))
        # 1.3. save data graph with middle infos
        mid_graph_save(mid_data_graph=data_graph, dataset_path=args.input)
    # 2. index construction
    if not is_indexed(args.input):
        print("\nNo available index!")
        print("Start index construction:")
        # 2.1. read middle data graph
        mid_data_graph = mid_graph_read(dataset_path=args.input)
        index_construction_start_timestamp = time.time()
        # 2.2. construct index
        index_root = construct_index(data_graph=mid_data_graph)
        print("Index construction time:", (time.time() - index_construction_start_timestamp))
        # 2.3. save the index json file
        index_save(index=index_root, dataset_path=args.input)
    # 3. online processing
    print("\nLoad precomputed data graph:")
    # 3.1. read middle data graph
    mid_data_graph = mid_graph_read(dataset_path=args.input)
    print("\nLoad constructed index:")
    # 3.2. read index
    index_root = index_read(dataset_path=args.input)
    print("\nStart online processing:")
    stat.start_timestamp = time.time()
    # 3.3. execute online processing
    result_set, total_diversity_score = execute_online(
        data_graph=mid_data_graph,
        query_keyword_Q=[int(keyword) for keyword in args.keywords.split(",")],
        query_support_k=args.support,
        radius_r=args.radius,
        threshold_theta=args.theta,
        query_L=args.top,
        nlparam=args.nlparam,
        index_root=index_root,
        optimal_mode=args.optimal,
        stat=stat
    )
    stat.obtainment_time = time.time() - stat.start_timestamp

    start_timestamp = time.time()
    # 3.4. refine the result set
    if args.diversity:
        print("\nStart refinement")
        result_set, total_diversity_score = execute_refine(
            query_L=args.top,
            data_graph=mid_data_graph,
            input_set=result_set,
            stat=stat
        )
    elif args.optimal:
        print("\nStart Optimal refinement")
        result_set, total_diversity_score = execute_refine_optimal(
            query_L=args.top,
            data_graph=mid_data_graph,
            input_set=result_set,
            stat=stat
        )
    elif args.naive:
        print("\nStart Naive refinement")
        result_set, total_diversity_score = execute_refine_without_pruning(
            query_L=args.top,
            data_graph=mid_data_graph,
            input_set=result_set,
            stat=stat
        )
    stat.refinement_time = time.time() - start_timestamp
    stat.finish_timestamp = time.time()
    stat.leaf_node_counter = count_leaf_node(index_root)
    stat.solver_result = list(result_set)
    stat.total_score = total_diversity_score
    for result in result_set:
        print(result[0], "with score:", result[1])
    # 4. save result set and statistic file
    result_graph_save(result_graph=[result[0] for result in result_set], dataset_path=args.input)
    statistic_file_save(stat=stat, dataset_path=args.input)
    print(stat.generate_stat_result())
