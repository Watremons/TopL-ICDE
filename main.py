from utils.argparser import args_parser
from utils.ioutils import data_graph_read, mid_graph_save, mid_graph_read, is_precomputed
from online.statistic import Statistics
from precompute import execute_offline
from process import execute_online


if __name__ == "__main__":
    stat = Statistics()
    args = args_parser()
    if not is_precomputed(args.input):
        data_graph = data_graph_read(args.input)
        data_graph, index_root = execute_offline(data_graph=data_graph)
        mid_graph_save(mid_data_graph=data_graph, index=index_root, dataset_path=args.input)
    else:
        mid_data_graph, index_root = mid_graph_read(dataset_path=args.input)
        result_set = execute_online(
            data_graph=mid_data_graph,
            query_keyword_Q=[int(keyword) for keyword in args.keywords.split(",")],
            query_support_k=args.support,
            radius_r=args.radius,
            threshold_theta=args.theta,
            query_L=args.top,
            index_root=index_root
        )
        stat.solver_result = [seed_community for (seed_community, _) in result_set]
        print(stat.solver_result)

# start: 19:02:30
