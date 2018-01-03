#!/bin/sh

module load system
module load singularity/2.4

for dir in $PI_HOME/frames2/*
do
    dir=${dir%*/}
    sbatch -p gpu --gres gpu:1 -t 4:00:00 --mail-type=FAIL --mail-user=sanchez7@stanford.edu --wrap="singularity exec --nv $SINGULARITY_CACHEDIR/openpose-latest.img bash -c 'cd /openpose-master && ./build/examples/openpose/openpose.bin --no_display true --render_pose 0 --face --hand --image_dir $PI_HOME/frames2/${dir##*/} --write_keypoint_json $PI_HOME/openpose_output/${dir##*/}'"
    sleep 1
done