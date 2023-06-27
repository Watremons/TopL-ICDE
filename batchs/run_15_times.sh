cd /home/watremons/projects/influential-community-detection/

conda activate topLICD

for ((i=0;i<15;i++))
do
python main.py -i dataset/manual/50000-145648-20-3 -Q 1,2,3,4,5 -k 4 -r 2 -t 0.2 -L 5
done