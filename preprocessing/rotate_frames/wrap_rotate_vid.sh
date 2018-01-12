#!/bin/sh

mkdir -p $PI_HOME/all_videos

for vid in $SCRATCH/globus/*/*; do

    outputvid=$PI_HOME/all_videos/$(basename $vid)

	if [[ $vid == *1205* || $vid == *1211* || $vid == *1225* || $vid == *1628*  ]]; then
	    echo "L $vid"
		sbatch -p normal,hns -t 3:00:00 --mail-type=FAIL --mail-user=sanchez7@stanford.edu \
		    --wrap="ffmpeg -i $vid -vf \"transpose=2,transpose=2\" $outputvid"
	else
	    echo "S $vid"
		sbatch -p normal,hns -t 2:00:00 --mail-type=FAIL --mail-user=sanchez7@stanford.edu \
		    --wrap="ffmpeg -i $vid -vf \"transpose=2,transpose=2\" $outputvid"
	fi
	sleep 1
done