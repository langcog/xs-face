#!/bin/sh
for dir in $PI_HOME/frames2/*
do
    dir=${dir%*/}
    sbatch -p normal,hns -t 2:00:00 --mail-type=FAIL --mail-user=sanchez7@stanford.edu --wrap="python rotate_frames.py ${dir##*/}"
    sleep 1
done