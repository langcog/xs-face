#!/bin/sh

module load tensorflow
module load opencv/3.0.0

for vid in $PI_HOME/frames_rotated/*; do
	if [[ $vid == *1205* || $vid == *1211* || $vid == *1225* || $vid == *1628*  ]]; then
	    echo "Large video (> 10GB): $vid"
		sbatch -p hns,normal -c 16 -t 20:00:00 --mail-type=FAIL --mail-user=sanchez7@stanford.edu \
		    --wrap="python detect_faces.py $vid"
	else
		sbatch -p hns,normal -c 8 -t 10:00:00 --mail-type=FAIL --mail-user=sanchez7@stanford.edu \
		    --wrap="python detect_faces.py $vid"
	fi
	sleep 1
done
