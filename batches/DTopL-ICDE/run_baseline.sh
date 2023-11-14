cd /home/yons/projects/influential-community-detection/

conda activate toplicde

for ((i=0;i<15;i++))
do
python main.py -i dataset/manual/50000-145648-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/50000-145648-20-3/gauss -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/manual/50000-145648-20-3/zipf -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5

python main.py -i dataset/realworld/amazon/334863-925872-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5
python main.py -i dataset/realworld/dblp_simple/317080-1049866-1000-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -d -n 5

done

for ((i=0;i<15;i++))
do
python main.py -i dataset/manual/50000-145648-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -N -n 5
python main.py -i dataset/manual/50000-145648-20-3/gauss -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -N -n 5
python main.py -i dataset/manual/50000-145648-20-3/zipf -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -N -n 5

python main.py -i dataset/realworld/amazon/334863-925872-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -N -n 5
python main.py -i dataset/realworld/dblp_simple/317080-1049866-1000-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -N -n 5

done


# for ((i=0;i<15;i++))
# do
# python main.py -i dataset/manual/50000-145648-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -o -n 5
# python main.py -i dataset/manual/50000-145648-20-3/gauss -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -o -n 5
# python main.py -i dataset/manual/50000-145648-20-3/zipf -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -o -n 5

# python main.py -i dataset/realworld/amazon/334863-925872-20-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -o -n 5
# python main.py -i dataset/realworld/dblp_simple/317080-1049866-1000-3 -Q 16,3,13,10,6 -k 4 -r 2 -t 0.2 -L 5 -o -n 5

# done
