#!/bin/sh
for i in $(seq 679 $END); 
do sbatch -p normal,hns -t 40:00 -c 16 --mail-type=FAIL --mail-user=sanchez7@stanford.edu --wrap="python detect_faces.py $i"
sleep 1 
done
