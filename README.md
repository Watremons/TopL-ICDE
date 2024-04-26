# influential-community-detection

Source code of "Top-L Most Influential Community Detection Over Social Networks", accepted by ICDE'24 - By Nan Zhang; Yutong Ye; Xiang Lian and Mingsong Chen.

## 0. enviroment

Python 3.11.5

## 1. Install

```bash
pip install pymetis
pip install networkx
pip install scipy
pip install numpy
# or
pip install -r requirements.txt
```

## 2. Input Data Format

Our input data is `*.gpickle.gz` format, which is packed by `nx.write_gpickle()`.

The input data in gz file can be read by `nx.readwrite.read_gpickle()` as a `nx.Graph`, which is implemented in the form of an adjacency list.

You can process the graph by the function in package `networkx`.

## 3. Usage

```bash
usage: main.py [-h] -i INPUT -Q KEYWORDS -k SUPPORT -r RADIUS -t THETA -L TOP [-d] [-n NLPARAM] [-o] [-N]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        the path of input file
  -Q KEYWORDS, --keywords KEYWORDS
                        a series of keywords separated commas, query keywords
  -k SUPPORT, --support SUPPORT
                        an integer, the support of seed communities
  -r RADIUS, --radius RADIUS
                        an integer, the maximum radius of seed communities
  -t THETA, --theta THETA
                        a float, the influence threshold
  -L TOP, --top TOP     an integer, the number of result seed communities
  -d, --diversity       use the diversity refinement
  -n NLPARAM, --nlparam NLPARAM
                        a integer, the number of nL approximation greedy algorithm
  -o, --optimal         use the optimal refinement
  -N, --naive           use the naive refinement
```

Some examples are as follows:

```bash
# manual result
# TopL-ICDE
python main.py -i dataset/manual/50000-145648-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5

# DTopL-ICDE
python main.py -i dataset/manual/50000-145648-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5

python main.py -i dataset/manual/50000-145648-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -N -n 5

python main.py -i dataset/manual/50000-145648-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -o -n 5

```

## Reference

[pymetis](https://github.com/inducer/pymetis)
[networkx](https://networkx.org/)
