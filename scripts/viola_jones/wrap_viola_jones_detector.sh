#!/bin/sh
for vid in $PI_HOME/frames4/*; do
	if [[ $vid == *1205* || $vid == *1211* || $vid == *1225* || $vid == *1628*  ]]; then
	    echo "Large video (> 10GB): $vid"
		sbatch -p hns,normal -c 16 -t 10:00:00 --mail-type=FAIL --mail-user=sanchez7@stanford.edu \
		    --wrap="python viola_jones_detector.py $vid"
	else
		sbatch -p hns,normal -c 8 -t 5:00:00 --mail-type=FAIL --mail-user=sanchez7@stanford.edu \
		    --wrap="python viola_jones_detector.py $vid"
	fi
	sleep 1
done
