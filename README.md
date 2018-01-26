Table of Contents
=================

   * [About](#about)
   * [Face detections](#face-detections)
      * [Preprocessing](#preprocessing)
      * [Face, Hand, Pose detection](#face-hand-pose-detection)
         * [MTCNN](#mtcnn)
         * [OpenPose](#openpose)
   * [Model Validation](#model-validation)
   * [Analysis](#analysis)
   * [Rendering the paper](#rendering-the-paper)


# About
The goal of this project was to analyze social information accessible to young children through headcam videos. The raw headcam data consists of 36 videos, one per subject, with the subjects belonging to 3 age groups: 8, 12, and 16 months (with equal subjects per group). The computational pipeline consists of first detecting faces in videos (where all video processing is done on [Sherlock](http://www.sherlock.stanford.edu), an HPC cluster available to Stanford faculty) and subsequently analyzing face detections along with posture and orientation annotations and demographics.

# Face detections
All face detections were done on Sherlock, using [SLURM](https://slurm.schedmd.com/) for job management. 

## Preprocessing
First steps involve moving the 36 xs-face videos to the computing environment of choice, in our case Sherlock. To do this we used [Globus](http://sherlock.stanford.edu/mediawiki/index.php/DTN). In Sherlock, the videos are located in the directory $PI_HOME/headcam_videos_original. Since the videos were recorded upside-down, we rotated all of them using scripts in [preprocessing](preprocessing). We then extracted frames using ffmpeg v3.5.1, which along with their rotated versions are located in $PI_HOME/frames and $PI_HOME/rotated_frames, respectively.

## Face, Hand, Pose detection

### MTCNN
Once all the frames were extracted, we ran the MTCNN [algorithm](https://github.com/kpzhang93/MTCNN_face_detection_alignment) using the mtnn [scripts](scripts/mtcnn). We used a Tensorflow implementation of the MTCNN algorithm found [here](https://github.com/davidsandberg/facenet). The script looks through every subject folder (i.e. "XS_0803") in the $PI_HOME/frames_rotated folder and runs the face detector (in a CPU env), which outputs a csv corresponding to that subject in a tmp folder. The csv contains the bounding box coordinates if a face was detected in the frame. Once all jobs finished, we combined the csvs in tmp to form a consolidated csv that was then stored [here](data/final_output).

### OpenPose
Unlike MTCNN, [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) did not work well on folders of frames (averaging about 28K per subject), but instead had its own utility for extracting frames and rotating them from videos, so that's what we used. In contrast to MTCNN which was run on the native Sherlock environment, we ran OpenPose through a docker container that already had the pre-compiled OpenPose binary. The Docker container with instructions on how to run it on Sherlock can be found [here](https://hub.docker.com/r/amsan7/openpose/). This binary must be run in a GPU environment. The output from OpenPose is stored in $PI_HOME/openpose_json_output, with a json file corresponding to every frame. The json stored the locations of 18 different body parts, 69 detailed face points, and 42 detailed hand points. In order to consolidate the json into one csv, we ran a script inside the [openpose](scripts/openpose) folder and stored the output in [final_output](data/final_output). However, this file was too large to save in git, so we instead uploaded a version to google drive. 

# Model Validation
In order to validate the models, we selected a sample of gold set images to annotate inside [ground_truth_creation](scripts/ground_truth_creation). These candidates were then downloaded from Sherlock onto my local machine, where they were annotated with a tool called [Rectlabel](https://rectlabel.com/). This tool created an annotation folder in every subject folder, containing all bounding box coordinates from the squares we drew in XML. The script inside [ground_truth_creation](scripts/ground_truth_creation) essentially extracted the face info from this setup and created a [ground truth](data/ground_truth/ground_truth3.csv) file. All analyses comparing this ground truth with actual results are in [analysis-validation](analysis-validation).

In order to not bias the evaluation because of the relatively rare appearance of faces in the dataset, two gold samples were selected: one high density sample consisting of a large number of face detections, and one random sample from the remaining frames. 

# Analysis
The final face detection results are stored in [final_output](data/final_output). These data were merged with the corresponding posture, orientation, and demographics csvs to form one large consolidated csv that is stored as a feather file in [data](data). 

# Rendering the paper
The Rmarkdown for the paper is stored inside the [writeup](writeup-cogsci) folder.
