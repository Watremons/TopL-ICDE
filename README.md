# influential-community-detection

influential-community-detection

## 1. install

```bash
pip install pymetis
pip install bitvector
pip install networkx
pip install bitvector
```

## 2. Usage

```bash
# manual result
python main.py -i dataset/manual/1000-4241-100-3 -Q 1,2,3,4,5 -k 5 -r 3 -t 0.1 -L 5
python main.py -i dataset/manual/10000-42517-1000-3 -Q 1,2,3,4,5 -k 5 -r 3 -t 0.1 -L 5
python main.py -i dataset/manual/50000-212790-1000-3 -Q 1,2,3,4,5 -k 5 -r 3 -t 0.1 -L 5

python main.py -i dataset/realworld/dblp/317080-1049866-1000-3 -Q 1,2,3,4,5 -k 5 -r 3 -t 0.1 -L 5
python main.py -i dataset/realworld/amazon/334863-925872-1000-3 -Q 1,2,3,4,5 -k 5 -r 3 -t 0.1 -L 5
python main.py -i dataset/realworld/epinions/75879-405740-1000-3 -Q 1,2,3,4,5 -k 5 -r 3 -t 0.1 -L 5
python main.py -i dataset/realworld/facebook/22470-170823-1000-3 -Q 1,2,3,4,5 -k 5 -r 3 -t 0.1 -L 5
# realworld result
```

## Reference

[pymetis](https://github.com/inducer/pymetis)
