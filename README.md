# xs-face
Analyzing the social information accessible to young children through headcam videos.

The final dataset consists of 36 subjects in 3 age groups: 8, 12, and 16 months, with 12 participants in each group. All video processing is done on [Sherlock](http://www.sherlock.stanford.edu), an HPC cluster available to Stanford faculty. 

The project can be split up into two parts: face detections & analysis.

## Face detections
All face detection work was done on Sherlock, using [SLURM](https://slurm.schedmd.com/) for job management. 

### Preprocessing
First steps involve moving the 36 xs-face videos to the computing environment of choice, in our case Sherlock. To do this we used [Globus](http://sherlock.stanford.edu/mediawiki/index.php/DTN). In Sherlock, the videos are located in the directory $PI_HOME/headcam_videos_original. Since the videos were recorded upside-down, we rotated all of them using scripts in /preprocessing. We then extracted frames using ffmpeg v3.5.1, which along with their rotated versions are located in $PI_HOME/frames and $PI_HOME/rotated_frames.

### Face, Hand, Pose detection

#### MTCNN
Once all the frames were extracted, we ran MTCNN using the scripts in /scripts/mtcnn. We used a Tensorflow implementation of the MTCNN algorithm found [here](https://github.com/davidsandberg/facenet). The script looks through every subject folder (i.e. "XS_0803") in the $PI_HOME/frames_rotated folder and runs the face detector (in a CPU env), which outputs a csv corresponding to that subject in a tmp folder. The csv contains the bounding box coordinates if a face was detected in the frame. Once all jobs finished, we combined the csvs in tmp to form a consolidated csv that was then stored in /data/final_output.

#### OpenPose
OpenPose did not work well on folders of frames (averaging about 28K per subject), but instead had its own utility for extracting frames and rotating them from videos, so that's what we used. In contrast to MTCNN which was run on the native Sherlock environment, we ran OpenPose through a docker container that already had the pre-compiled OpenPose binary. The Docker container with instructions on how to run it on Sherlock can be found [here](https://hub.docker.com/r/amsan7/openpose/). This binary must be run in a GPU environment. The output from OpenPose is stored in $PI_HOME/openpose_json_output, with a json file corresponding to every frame. The json stored the locations of 18 different body parts, 69 detailed face points, and 42 detailed hand points. In order to consolidate the json into one csv, I ran a script inside /scripts/openpose and stored the output in data/final_output. However, this file was too large to save in git, so I instead uploaded a version to google drive. 

## Model Validation
In order to validate the models, we selected a sample of gold set images to annotate inside /scripts/ground_truth_creation. These candidates were then downloaded from Sherlock onto my local machine, where they were annotated with a tool called [Rectlabel](https://rectlabel.com/). This tool created an annotation folder in every subject folder, containing all bounding box coordinates from the squares we drew. The script inside /scripts/ground_truth_creation essentially extracts the face info from this setup and creates a file called data/ground_truth.csv. All analyses comparing this ground truth with actual results are in /analysis-validation.

In order to not bias the evaluation considering the relatively rare appearance of faces in the dataset, two samples were selected: one high density sample consisting of a large number of face detections, and one random sample from the remaining frames. 

## Analysis
The final face detection results are stored in data/final_output (MTCNN, OpenPose). These data were merged with the corresponing posture, orientation, and demographics csvs to form one large consolidated csv that was too large to store in git and is instead stored in google drive. 
