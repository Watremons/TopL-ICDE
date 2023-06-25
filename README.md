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
python main.py -i dataset/manual/1000-5649-100-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
# done
python main.py -i dataset/manual/10000-42517-1000-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/10000-42517-1000-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/10000-42517-1000-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5

# todo
python main.py -i dataset/manual/30000-127741-1000-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/30000-127741-1000-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/30000-127741-1000-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5

# done
python main.py -i dataset/manual/50000-212790-500-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-500-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-500-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5

# done
python main.py -i dataset/manual/50000-212790-800-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-800-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-800-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5

# done
python main.py -i dataset/manual/50000-212790-1000-1 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-1000-1/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-1000-1/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5

# done
python main.py -i dataset/manual/50000-212790-1000-2 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-1000-2/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-1000-2/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5

python main.py -i dataset/manual/50000-212790-1000-3 -Q 1,2,3,4,5 -k 5 -r 2 -t 0.08 -L 5
# done
python main.py -i dataset/manual/50000-212790-1000-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-1000-3 -Q 1,2,3,4,5 -k 5 -r 3 -t 0.1 -L 5
python main.py -i dataset/manual/50000-212790-1000-3/gauss -Q 1,2,3,4,5 -k 5 -r 3 -t 0.1 -L 5
python main.py -i dataset/manual/50000-212790-1000-3/zipf -Q 1,2,3,4,5 -k 5 -r 3 -t 0.1 -L 5

# done
python main.py -i dataset/manual/50000-212790-1000-4 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-1000-4/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-1000-4/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5

# done
python main.py -i dataset/manual/50000-212790-1000-5 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-1000-5/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-1000-5/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5

# done
python main.py -i dataset/manual/50000-212790-2000-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-2000-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-2000-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5

# done
python main.py -i dataset/manual/50000-212790-5000-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-5000-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/50000-212790-5000-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5


python main.py -i dataset/manual/100000-249917-1000-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5

# done
python main.py -i dataset/manual/100000-426096-1000-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/100000-426096-1000-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/100000-426096-1000-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5

# done
python main.py -i dataset/manual/500000-2129290-1000-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/500000-2129290-1000-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/500000-2129290-1000-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5

# done
python main.py -i dataset/manual/1000000-4259490-1000-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/1000000-4259490-1000-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
python main.py -i dataset/manual/1000000-4259490-1000-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5

# realworld result
# done
python main.py -i dataset/realworld/dblp_simple/317080-1049866-1000-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
# done
python main.py -i dataset/realworld/amazon_simple/334863-925872-1000-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.08 -L 5
```

## Reference

[pymetis](https://github.com/inducer/pymetis)
