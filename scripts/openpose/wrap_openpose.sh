#!/bin/sh

module load system
module load singularity/2.4

mkdir -p $PI_HOME/openpose_output2

for vid in $PI_HOME/frames4/*; do
	if [[ $vid == *1205* || $vid == *1211* || $vid == *1225* || $vid == *1628*  ]]; then
	    echo "Large video (> 10GB): $vid"
	    time=2-00:00:00
	else
	    echo "Small vid: $vid"
	    time=2-00:00:00
	fi

    output_dir=$PI_HOME/openpose_output2/$(basename $vid)
	mkdir -p $output_dir

	sbatch -p gpu --gres gpu:1 -t $time --mail-type=FAIL --mail-user=sanchez7@stanford.edu \
	    --wrap="singularity exec --nv $SINGULARITY_CACHEDIR/openpose-latest.img bash -c \
	        'cd /openpose-master && ./build/examples/openpose/openpose.bin \
	            --no_display true \
                --render_pose 0 \
                --image_dir $vid \
                --write_keypoint_json $output_dir'"

	sleep 1
done
