#!/bin/sh

for vid in $PI_HOME/openpose_output6/*; do
	if [[ $vid == *1205* || $vid == *1211* || $vid == *1225* || $vid == *1628*  ]]; then
	    echo "Large video (> 10GB): $vid"
	    time=3:00:00
	    memory=12G
	else
	    echo "Small vid: $vid"
	    time=2:00:00
	    memory=4G
	fi

	sbatch -p normal,hns -t $time --mem $memory --mail-type=FAIL --mail-user=sanchez7@stanford.edu \
	    --wrap="python json_to_csv.py $vid"
    sleep 1
done