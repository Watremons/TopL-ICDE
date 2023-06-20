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
python main.py -i dataset/manual/50000-124933-1000-3 -Q 1,2,3,4,5 -k 2 -r 3 -t 0.2 -L 5

# realworld result
python main.py -i dataset/realworld/dblp/317080-1049866-1000-3 -Q 1,2,3,4,5 -k 2 -r 3 -t 0.2 -L 5
python main.py -i dataset/realworld/youtube/1134890-2987624-1000-3 -Q 1,2,3,4,5 -k 2 -r 3 -t 0.2 -L 5
```
## Reference

[pymetis](https://github.com/inducer/pymetis)