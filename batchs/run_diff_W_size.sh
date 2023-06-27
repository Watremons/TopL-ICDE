cd /home/watremons/projects/influential-community-detection/

conda activate topLICD

for ((i=0;i<15;i++))
do
python main.py -i dataset/manual/50000-145648-20-1 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-1/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-1/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5

python main.py -i dataset/manual/50000-145648-20-2 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-2/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-2/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5

python main.py -i dataset/manual/50000-145648-20-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-3/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-3/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5

python main.py -i dataset/manual/50000-145648-20-4 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-4/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-4/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5

python main.py -i dataset/manual/50000-145648-20-5 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-5/gauss -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
python main.py -i dataset/manual/50000-145648-20-5/zipf -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5

done