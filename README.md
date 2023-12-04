# influential-community-detection

influential-community-detection

## 0. enviroment

Python 3.11.5

## 1. install

```bash
pip install pymetis
pip install networkx
pip install scipy
pip install numpy
# or
pip install -r requirements.txt
```

## 2. Usage

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
