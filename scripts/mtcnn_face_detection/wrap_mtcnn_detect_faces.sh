#!/bin/sh
for i in $(seq 175 $END);
do sbatch -p normal,hns -t 1:30:00 -c 8 --mail-type=FAIL --mail-user=sanchez7@stanford.edu --wrap="python detect_faces.py $i"
sleep 1 
done
