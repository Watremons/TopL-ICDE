cd /home/yons/projects/influential-community-detection/

conda activate topLICD

for ((i=0;i<15;i++))
do
python main.py -i dataset/manual/10000-28675-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/10000-28675-20-3/gauss -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/10000-28675-20-3/zipf -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5

python main.py -i dataset/manual/25000-72201-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/25000-72201-20-3/gauss -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/25000-72201-20-3/zipf -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5

python main.py -i dataset/manual/50000-145648-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/50000-145648-20-3/gauss -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/50000-145648-20-3/zipf -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5

python main.py -i dataset/manual/100000-295840-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/100000-295840-20-3/gauss -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/100000-295840-20-3/zipf -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5

python main.py -i dataset/manual/250000-768545-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/250000-768545-20-3/gauss -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/250000-768545-20-3/zipf -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5

python main.py -i dataset/manual/500000-1616753-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/500000-1616753-20-3/gauss -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/500000-1616753-20-3/zipf -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5

python main.py -i dataset/manual/1000000-3500118-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/1000000-3500118-20-3/gauss -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/1000000-3500118-20-3/zipf -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
done