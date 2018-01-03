#!/bin/sh
for dir in $PI_HOME/headcam_final/*
do
    dir=${dir%*/}
    sbatch -p normal,hns -t 1:30:00 --mem=8G --mail-type=FAIL --mail-user=sanchez7@stanford.edu --wrap="python extract_frames.py ${dir##*/}"
    sleep 1
done