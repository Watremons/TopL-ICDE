cd /home/watremons/projects/influential-community-detection/

conda activate topLICD

for ((i=0;i<15;i++))
do
python main.py -i dataset/manual/50000-145648-20-3 -Q 16,3,13,10,6 -k 4 -r 1 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-3/gauss -Q 16,3,13,10,6 -k 4 -r 1 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-3/zipf -Q 16,3,13,10,6 -k 4 -r 1 -t 0.2 -L 5

python main.py -i dataset/manual/50000-145648-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-3/gauss -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-3/zipf -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5

python main.py -i dataset/manual/50000-145648-20-3 -Q 16,3,13,10,6 -k 4 -r 3 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-3/gauss -Q 16,3,13,10,6 -k 4 -r 3 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-3/zipf -Q 16,3,13,10,6 -k 4 -r 3 -t 0.2 -L 5

done