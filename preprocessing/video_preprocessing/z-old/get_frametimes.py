#!/usr/bin/env python                                                          

# run this on the server for all movies to get parsed FFMPEG output files

import sys, os, subprocess

target = sys.argv[1]
destination = sys.argv[2]

print("target: " + target + "\n")
print("destination: " + destination + "\n")

targetfiles = os.listdir(target)

for file in targetfiles:
    if file.find(".mp4") > 0: # if this is a movie                             \
                                                                                
	dirname = file.replace(".mp4","")
	print "***********" + dirname + "**********"

	f = open(destination + "/" + file + ".frames.txt","w")
	subprocess.call(["ffprobe",target + "/" + file,"-show_packets"],stdout=\
\
f)
