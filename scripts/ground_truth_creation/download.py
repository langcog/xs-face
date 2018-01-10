import os
import csv

with open("../../data/gold_set_candidates.csv", 'rb') as img_paths_f:
        img_paths = list(csv.reader(img_paths_f, delimiter=','))

for path in img_paths[1:]:
	os.system("mkdir -p ~/xsface/sample_images2/%s" % (path[1]))
	os.system("scp sanchez7@sherlock.stanford.edu:/home/groups/mcfrank/frames4/%s ~/xsface/sample_images2/%s" % (path[9], path[1]))

