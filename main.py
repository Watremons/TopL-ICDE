import time

from utils.argparser import args_parser
from utils.ioutils import data_graph_read, mid_graph_save, mid_graph_read, is_precomputed, result_graph_save, statistic_file_save
from online.statistics import Statistics
from precompute import execute_offline
from process import execute_online


if __name__ == "__main__":
    args = args_parser()
    stat = Statistics(
        input_file_folder=args.input,
        query_keyword_Q=[int(keyword) for keyword in args.keywords.split(",")],
        query_support_k=args.support,
        radius_r=args.radius,
        threshold_theta=args.theta,
        query_L=args.top,
    )
    print("Start offline pre-computation:")
    if not is_precomputed(args.input):
        data_graph = data_graph_read(args.input)
        data_graph, index_root = execute_offline(data_graph=data_graph)
        mid_graph_save(mid_data_graph=data_graph, index=index_root, dataset_path=args.input)
    print("Start online processing:")
    mid_data_graph, index_root = mid_graph_read(dataset_path=args.input)
    stat.start_timestamp = time.time()
    result_set = execute_online(
        data_graph=mid_data_graph,
        query_keyword_Q=[int(keyword) for keyword in args.keywords.split(",")],
        query_support_k=args.support,
        radius_r=args.radius,
        threshold_theta=args.theta,
        query_L=args.top,
        index_root=index_root,
        stat=stat
    )
    stat.finish_timestamp = time.time()
    stat.solver_result = list(result_set)
    for result in result_set:
        print(result)
        print(result[0])
        print(result[1])
    result_graph_save(result_graph=[result[0] for result in result_set], dataset_path=args.input)
    statistic_file_save(stat=stat, dataset_path=args.input)
    print(stat.generate_stat_result())
