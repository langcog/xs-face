# xs-face
Headcam video analysis

All video processing is done on [Sherlock](www.sherlock.stanford.edu). Two face detection systems are used:
* A Tensorflow [implementation](https://github.com/davidsandberg/facenet) of the MTCNN face detection algorithm found [here](https://github.com/kpzhang93/MTCNN_face_detection_alignment)
* OpenPose face, hand, and pose detectors found [here](https://github.com/CMU-Perceptual-Computing-Lab/openpose/)

## Preprocessing
36 videos of 8, 12, and 16 month olds are stored at $PI_HOME/headcam_final. I ran ffmpeg scripts to extract frames and placed them in $PI_HOME/frames. I then rotated each frame because the original orientation was upside down. Scripts jotting down the fps, number of frames, and length are inside /preprocessing; regular checks against original metadata should be done periodically and throughout the pipeline. Note: there are still some discrepancies between number of frames outputted with ffprobe and those actually extracted with ffmpeg.

## Face, Hand, Pose Detection
SLURM jobs are used to process images on a GPU. Whereas the MTCNN detector is straighforward with all code and models included in the repo, OpenPose is ran inside of a docker image found [here](https://hub.docker.com/r/amsan7/openpose/). Instructions on how to get the image running with [Singularity](http://singularity.lbl.gov/), which is the only container management system on Sherlock, can be found in the DockerHub link. After output is written to the data/tmp folder, it is then processed and combined into a single CSV with scripts inside their respective model folders. Still need to rerun models after frame issue is fixed.

## Validation
More work needs to be done here - but we've so far used [RectLabel](https://rectlabel.com/) to label around 500 images. the face annotations are located inside data/ground_truth. TODO - develop a better process to select and annotate images, and then import those annotations for comparison in Analysis.

## Analysis
TBD
