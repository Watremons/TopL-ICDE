import argparse


def args_parser():
    parser = argparse.ArgumentParser()
    # federated arguments
    parser.add_argument("-i", "--input", type=str, help="the path of input file")
    parser.add_argument("-Q", "--keywords", type=str, help="a series of keywords separated commas, query keywords")
    parser.add_argument("-k", "--support", type=int, help="an integer, the support of seed communities")
    parser.add_argument("-r", "--radius", type=int, help="an integer, the maximum radius of seed communities")
    parser.add_argument("-t", "--theta", type=float, help="a float, the influence threshold")
    parser.add_argument("-L", "--top", type=int, help="an integer, the number of result seed communities")
    # parser.add_argument('--weight_decay', type=float, default=1e-4, help="weight_decay (default: 1e-4)")
    # parser.add_argument('--split', type=str, default='user', help="train-test split type, user or sample")

    args = parser.parse_args()
    return args
