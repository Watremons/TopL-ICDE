import os


class Statistics:
    """
    Class:
        A class which used for record the statistic data
    Attributes:
        input_file_name: the file name of the input cnf file
        output_file_name: the file name of the output result file
        output_stat_file_name: the file name of the statistic data file
        solver_result: the result of SAT problem for the input(SAT or UNSAT)
        edge_num: the number of graph edge
        node_num: the number of graph node
        start_timestamp: the timestamp of the beginning
        finish_timestamp: the timestamp of the end

    """
    def __init__(
        self,
        input_file_folder: str,
        diversity: bool,
        optimal: bool,
        naive: bool,
        query_keyword_Q: list,
        query_support_k: int,
        radius_r: int,
        threshold_theta: float,
        query_L: int,
        nlparam: int
    ) -> None:
        """
        Method:
            Constructed Method
        """
        self.input_file_name = os.path.join(input_file_folder, "data_graph.gpickle.gz")
        self.mid_file_name = os.path.join(input_file_folder, "mid_data_graph.gpickle.gz")
        self.index_file_name = os.path.join(input_file_folder, "index.json")
        self.output_stat_file_name = os.path.join(input_file_folder, "statistics.txt")

        self.solver_result = []
        self.total_score = 0
        distribution = "uniform"
        input_info = input_file_folder.split('/')[-1].split('-')
        if len(input_info) < 2:
            input_info = input_file_folder.split('/')[-2].split('-')
            distribution = input_file_folder.split('/')[-1]
        self.node_num = input_info[0]
        self.edge_num = input_info[1]
        self.all_keywords_num = input_info[-2]
        self.keywords_per_vertex = input_info[-1]
        self.distribution = distribution
        self.refine_type = "No Refine"
        if diversity:
            self.refine_type = "Diversity"
        elif optimal:
            self.refine_type = "Optimal"
        elif naive:
            self.refine_type = "Naive"
        else:
            self.refine_type = "No Refine"
        self.query_keyword_Q = query_keyword_Q
        self.query_support_k = query_support_k
        self.radius_r = radius_r
        self.threshold_theta = threshold_theta
        self.query_L = query_L
        self.nlparam = nlparam

        self.start_timestamp = 0
        self.finish_timestamp = 0

        self.select_greatest_entry_in_H_time = 0
        self.leaf_node_traverse_time = 0
        self.nonleaf_node_traverse_time = 0
        self.compute_r_hop_time = 0
        self.compute_k_truss_time = 0
        self.compute_influential_score_time = 0
        self.modify_result_set_time = 0
        self.obtainment_time = 0
        self.refinement_time = 0

        self.select_greatest_increment_entry_time = 0
        self.refinement_increment_compute_time = 0
        self.refinement_increment_compute_counter = 0
        self.refinement_graph_update_time = 0
        self.refinement_grah_copy_time = 0

        self.vertex_pruning_counter = 0
        self.entry_pruning_counter = 0
        self.leaf_node_counter = 0
        self.leaf_node_visit_counter = 0

        self.optimal_sampling_ratio = 1

    def generate_stat_result(self) -> str:
        """
        Method:
            Return the statistic result as string
        """
        result = ""
        result += "STATISTIC RESULT\n"
        result += "-------------FILE INFO-------------\n"
        result += "Input File: {}\n".format(self.input_file_name)
        result += "Mid Data File: {}\n".format(self.mid_file_name)
        result += "Index File: {}\n".format(self.index_file_name)
        result += "Statistic File: {}\n".format(self.output_stat_file_name)
        result += "\n"
        result += "-------------SOLVER INFO-------------\n"
        result += "Result: {}\n".format([result[1] for result in self.solver_result])
        result += "Total Score: {}\n".format(self.total_score)
        result += "Total Nodes: {}\n".format(self.node_num)
        result += "Total Edges: {}\n".format(self.edge_num)
        result += "All Keywords: {}\n".format(self.all_keywords_num)
        result += "Keywords Per Vertex: {}\n".format(self.keywords_per_vertex)
        result += "Distribution: {}\n".format(self.distribution)
        result += "\n"
        result += "-------------QUERY INFO-------------\n"
        result += "Query Keywords: {}\n".format(self.query_keyword_Q)
        result += "Query Support: {}\n".format(self.query_support_k)
        result += "Query Radius: {}\n".format(self.radius_r)
        result += "Query Threshold: {}\n".format(self.threshold_theta)
        result += "Query L: {}\n".format(self.query_L)
        result += "\n"
        result += "-------------Pruning INFO-------------\n"
        result += "Pruning Vertices: {}\n".format(self.vertex_pruning_counter)
        result += "Pruning Entries: {}\n".format(self.entry_pruning_counter)
        result += "Leaf Nodes: {}\n".format(self.leaf_node_counter)
        result += "Pruning Leaf Nodes: {}\n".format(self.leaf_node_counter - self.leaf_node_visit_counter)
        result += "\n"
        result += "-------------REFINE INFO-------------\n"
        result += "Refine Type: {}\n".format(self.refine_type)
        result += "Query n: {}\n".format(self.nlparam)
        result += "-------------TIME INFO-------------\n"
        result += "Started at: {} \tFinished at: {}\n".format(self.start_timestamp, self.finish_timestamp)
        result += "Total time: {}\n".format(self.finish_timestamp - self.start_timestamp)
        result += "Obtainment time: {}\n".format(self.obtainment_time)
        result += "Refinement time: {}\n".format(self.refinement_time)
        result += "-------------OBTAIN TIME INFO-------------\n"
        result += "Select Greatest Entry in Heap time: {}\n".format(self.select_greatest_entry_in_H_time)
        result += "Leaf Node Traverse time: {}\n".format(self.leaf_node_traverse_time)
        result += "NonLeaf Node Traverse time: {}\n".format(self.nonleaf_node_traverse_time)
        result += "Compute R-Hop time: {}\n".format(self.compute_r_hop_time)
        result += "Compute K-Truss time: {}\n".format(self.compute_k_truss_time)
        result += "Compute Influential Score time: {}\n".format(self.compute_influential_score_time)
        result += "Modify Result Set time: {}\n".format(self.modify_result_set_time)
        result += "-------------REFINE TIME INFO-------------\n"
        result += "Select Greatest Increment Entry in Heap time: {}\n".format(self.select_greatest_increment_entry_time)
        result += "Refinement Increment Compute Time: {} for {} times\n".format(self.refinement_increment_compute_time, self.refinement_increment_compute_counter)
        result += "Optimal Sampling Ratio: {}\n".format(self.optimal_sampling_ratio)
        result += "Refinement Graph Update Time: {}\n".format(self.refinement_graph_update_time)
        result += "Refinement Graph Copy Time: {}\n".format(self.refinement_grah_copy_time)
        return result
