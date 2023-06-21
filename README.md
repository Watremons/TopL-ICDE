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

python main.py -i dataset/realworld/dblp/317080-1049866-1000-3 -Q 1,2,3,4,5 -k 6 -r 3 -t 0.1 -L 5

# realworld result
```
## Reference

[pymetis](https://github.com/inducer/pymetis)
