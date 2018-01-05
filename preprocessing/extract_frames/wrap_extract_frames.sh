#!/bin/bash

for vid in $SCRATCH/globus/*/*; do
	if [[ $vid == *1205* || $vid == *1211* || $vid == *1225* || $vid == *1628*  ]]; then
	    # Large video (> 10GB)
		sbatch -p normal,hns -t 2:00:00 --mem=24G --mail-type=FAIL --mail-user=sanchez7@stanford.edu \
		    --wrap="python extract_frames.py $vid"
	else
	    echo "S $vid"
		sbatch -p normal,hns -t 1:30:00 --mail-type=FAIL --mail-user=sanchez7@stanford.edu \
		    --wrap="python extract_frames.py $vid"
	fi
	sleep 1
done 
