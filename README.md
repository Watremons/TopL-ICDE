# influential-community-detection

influential-community-detection

## 1. install

```bash
pip install pymetis
pip install networkx
```

## 2. Usage

```bash
# manual result
# TopL-ICDE
python main.py -i dataset/manual/50000-145648-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-3/gauss -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-3/zipf -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5

# DTopL-ICDE
python main.py -i dataset/manual/50000-145648-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/50000-145648-20-3/gauss -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/50000-145648-20-3/zipf -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5

python main.py -i dataset/manual/50000-145648-20-5 -Q 16,3,13,10,6,2,12,14,3,19 -k 4 -r 2 -t 0.2 -L 5 -d -n 5

python main.py -i dataset/manual/50000-145648-20-5 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 10 -d -n 5

# realworld result
python main.py -i dataset/realworld/dblp/317080-1049866-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/realworld/dblp/317080-1049866-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
# python main.py -i dataset/realworld/dblp_simple/317080-1049866-1000-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5
# python main.py -i dataset/realworld/dblp_simple/317080-1049866-1000-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 2 


python main.py -i dataset/realworld/amazon/334863-925872-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/realworld/amazon/334863-925872-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5

# python main.py -i dataset/realworld/amazon_simple/317080-1049866-1000-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5
```

## Reference

[pymetis](https://github.com/inducer/pymetis)
