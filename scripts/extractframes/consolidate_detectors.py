#!/usr/bin/env python
# run this to consolidate face detectors

import glob

target = "../data/detectors/*.txt"
destination = "../data/all_detectors.csv"

outfile = open(destination,"w")
outfile.write("subid,frame,face,x,y,w,h\n")

for fname in glob.glob(target):
	print fname
	infile = open(fname, "r")
	subid = "XS_" + fname[-8:-4]

	for line in infile.readlines():
		[f, x, y, w, h, conf] = line.replace("NaN","NA").split(" ")


		if x == "NA":
			face = "FALSE"
		else:
			face = "TRUE"

		outfile.write("{},{},{},{},{},{},{}\n".format(subid, f, face, x, y, w, h))


	infile.close()
