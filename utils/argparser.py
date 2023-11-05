import argparse


def args_parser():
    parser = argparse.ArgumentParser()
    # federated arguments
    parser.add_argument("-i", "--input", type=str, required=True, help="the path of input file")
    parser.add_argument("-Q", "--keywords", type=str, required=True, help="a series of keywords separated commas, query keywords")
    parser.add_argument("-k", "--support", type=int, required=True, help="an integer, the support of seed communities")
    parser.add_argument("-r", "--radius", type=int, required=True, help="an integer, the maximum radius of seed communities")
    parser.add_argument("-t", "--theta", type=float, required=True, help="a float, the influence threshold")
    parser.add_argument("-L", "--top", type=int, required=True, help="an integer, the number of result seed communities")
    parser.add_argument("-d", "--diversity", action="store_true", help="use the diversity refinement")
    parser.add_argument("-n", "--nlparam", type=int, default=1, help="a integer, the number of nL approximation greedy algorithm")
    args = parser.parse_args()
    return args
