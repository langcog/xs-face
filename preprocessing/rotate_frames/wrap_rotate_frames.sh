#!/bin/sh

for vid in $PI_HOME/frames3/*; do
	if [[ $vid == *1205* || $vid == *1211* || $vid == *1225* || $vid == *1628*  ]]; then
	    # Large video (> 10GB)
	    echo "L $vid"
		sbatch -p normal,hns -t 3:00:00 --mail-type=FAIL --mail-user=sanchez7@stanford.edu \
		    --wrap="python rotate_frames.py $vid"
	else
		sbatch -p normal,hns -t 2:00:00 --mail-type=FAIL --mail-user=sanchez7@stanford.edu \
		    --wrap="python rotate_frames.py $vid"
	fi
	sleep 1
done