#!/bin/sh

module load tensorflow.1/1.3.0

for i in $(seq 175 $END);
do sbatch -p hns_gpu,gpu --gres gpu:4 -t 45:00 --mail-type=FAIL --mail-user=sanchez7@stanford.edu --wrap="python detect_faces_openpose.py $i"
sleep 1
done