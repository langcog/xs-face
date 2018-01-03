#!/bin/sh
for dir in $PI_HOME/openpose_output/*
do
    dir=${dir%*/}
    sbatch -p normal,hns -t 2:00:00 --mail-type=FAIL --mail-user=sanchez7@stanford.edu --wrap="python json_to_csv.py ${dir##*/}"
    sleep 1
done