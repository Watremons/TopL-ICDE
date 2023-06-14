import argparse


def args_parser():
    parser = argparse.ArgumentParser()
    # federated arguments
    parser.add_argument("-i", "--input", type=str, default='./dataset/', help="the path of input file")
    # parser.add_argument('--weight_decay', type=float, default=1e-4, help="weight_decay (default: 1e-4)")
    # parser.add_argument('--split', type=str, default='user', help="train-test split type, user or sample")

    args = parser.parse_args()
    return args
