#!/bin/bash

for vid in $PI_HOME/xs-face/headcam_videos_original/*; do
	sbatch -p normal,hns -t 35:00 --mail-type=FAIL --mail-user=sanchez7@stanford.edu \
        --wrap="ffprobe -show_frames -select_streams v:0 $vid > $(basename $vid).frames.txt"
	sleep 1
done
