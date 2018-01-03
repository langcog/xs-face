import os
import csv

with open("../sample.csv", 'rb') as img_paths_f:
        img_paths = list(csv.reader(img_paths_f, delimiter=','))

for path in img_paths[1:]:
	os.system("mkdir -p ~/xsface/sample_images/%s/%s" % (path[0], path[1]))
	os.system("scp sanchez7@sherlock.stanford.edu:%s ~/xsface/sample_images/%s/%s" % (path[9], path[0], path[1]))

