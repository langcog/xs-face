import os
import csv

with open("../../data/ground_truth/gold_set_candidates_from_openpose.csv", 'rb') as img_paths_f:
        img_paths = list(csv.reader(img_paths_f, delimiter=','))

for path in img_paths[1:]:
    os.system("mkdir -p ~/xsface/sample_face_images_openpose/%s" % (path[1]))
    os.system("scp sanchez7@sherlock.stanford.edu:/share/PI/mcfrank/frames_rotated/%s ~/xsface/sample_face_images_openpose/%s" % (path[8], path[1]))

