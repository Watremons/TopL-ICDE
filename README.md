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
# done
python main.py -i dataset/manual/10000-28675-20-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/10000-28675-20-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/10000-28675-20-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5

# todo
python main.py -i dataset/manual/25000-72201-20-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/25000-72201-20-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/25000-72201-20-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5

# done
python main.py -i dataset/manual/50000-145648-20-1 -Q 1,2,3,4,5 -k 5 -r 3 -t 0.3 -L 5
python main.py -i dataset/manual/50000-145648-20-1/gauss -Q 1,2,3,4,5 -k 5 -r 2 -t 0.3 -L 5
python main.py -i dataset/manual/50000-145648-20-1/zipf -Q 1,2,3,4,5 -k 5 -r 2 -t 0.3 -L 5

# done
python main.py -i dataset/manual/50000-145648-20-2 -Q 1,2,3,4,5 -k 5 -r 3 -t 0.3 -L 5
python main.py -i dataset/manual/50000-145648-20-2/gauss -Q 1,2,3,4,5 -k 5 -r 2 -t 0.3 -L 5
python main.py -i dataset/manual/50000-145648-20-2/zipf -Q 1,2,3,4,5 -k 5 -r 2 -t 0.3 -L 5

# done
python main.py -i dataset/manual/50000-145648-10-3 -Q 1,2,3,4,5 -k 5 -r 3 -t 0.3 -L 5
python main.py -i dataset/manual/50000-145648-10-3/gauss -Q 1,2,3,4,5 -k 5 -r 2 -t 0.3 -L 5
python main.py -i dataset/manual/50000-145648-10-3/zipf -Q 1,2,3,4,5 -k 5 -r 2 -t 0.3 -L 5

# done
python main.py -i dataset/manual/50000-145648-20-3 -Q 1,2,3,4,5 -k 5 -r 3 -t 0.3 -L 5
python main.py -i dataset/manual/50000-145648-20-3/gauss -Q 1,2,3,4,5 -k 5 -r 2 -t 0.3 -L 5
python main.py -i dataset/manual/50000-145648-20-3/zipf -Q 1,2,3,4,5 -k 5 -r 2 -t 0.3 -L 5

# done
python main.py -i dataset/manual/50000-145648-50-3 -Q 1,2,3,4,5 -k 5 -r 3 -t 0.3 -L 5
python main.py -i dataset/manual/50000-145648-50-3/gauss -Q 1,2,3,4,5 -k 5 -r 2 -t 0.3 -L 5
python main.py -i dataset/manual/50000-145648-50-3/zipf -Q 1,2,3,4,5 -k 5 -r 2 -t 0.3 -L 5

# done
python main.py -i dataset/manual/50000-145648-80-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-80-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-80-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5

# done
python main.py -i dataset/manual/50000-145648-80-4 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-80-4/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-80-4/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5

# done
python main.py -i dataset/manual/50000-145648-80-5 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-80-5/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-80-5/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5

# done
python main.py -i dataset/manual/100000-295840-20-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/100000-295840-20-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/100000-295840-20-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5

# done
python main.py -i dataset/manual/500000-1616753-20-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/500000-1616753-20-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/500000-1616753-20-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5

# done
python main.py -i dataset/manual/1000000-3500118-20-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/1000000-3500118-20-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/1000000-3500118-20-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5

# realworld result
# done
python main.py -i dataset/realworld/dblp/317080-1049866-20-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
# done
python main.py -i dataset/realworld/amazon/334863-925872-20-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
```

## Reference

[pymetis](https://github.com/inducer/pymetis)
