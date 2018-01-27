#!/bin/sh

module load system
module load singularity/2.4
module load cuda/8.0.61
module load caffe2/0.8.1
module load cudnn/5.1

mkdir -p $PI_HOME/openpose_json_output

for vid in $SCRATCH/globus/*/*; do
	if [[ $vid == *1205* || $vid == *1211* || $vid == *1225* || $vid == *1628*  ]]; then
	    echo "Large video (> 10GB): $vid"
	    time=10:00:00
	    memory=64G
	else
	    echo "Small vid: $vid"
	    time=5:00:00
	    memory=8G
	fi

    output_dir=$PI_HOME/openpose_output6/$(basename $vid)
	mkdir -p $output_dir

	sbatch -p gpu --gres gpu:1 -t $time --mem $memory --mail-type=FAIL --mail-user=sanchez7@stanford.edu \
	    --wrap="singularity exec --nv $SINGULARITY_CACHEDIR/openpose-latest.img bash -c \
	        'cd /openpose-master && ./build/examples/openpose/openpose.bin \
	        --no_display true \
            --render_pose 0 \
            --video $vid \
            --frame_rotate 180 \
	    --face \
	    --hand \
            --write_keypoint_json $output_dir'"

	sleep 1
done
