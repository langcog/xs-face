#!/usr/bin/env python

# run this locally to take FFMPEG packet files and get the actual timestamps for frames

import os, sys, re
from PyRTF import *

target = sys.argv[1]
targetfiles = os.listdir(target + "/raw")
#print target
#print targetfiles

checkfile = open("../data/movie_lengths.csv","a")
checkfile.write("subid,last.frame,length\n")

for f in filter (lambda a: a.find(".txt") != -1, targetfiles):
    # print f
    fin = open(target + "/raw/" + f,"r")
    short_f = f[3:7] + ".csv"
    fout = open(target + "/" + short_f,"w")
    fout.write("frame,time\n")
    
    contents = fin.read().split("[PACKET]")

    i = 1
    for c in contents:
        if c.find("codec_type=video") != -1:
            m = re.search(r"pts_time=\d+.\d+",c)
            if m != None:
                fout.write(str(i) + "," + m.group(0).replace("pts_time=","") + "\n")
                i = i + 1

    checkfile.write("XS-" + short_f + "," + str(i-1) + "," + m.group(0).replace("pts_time=","") + "\n")
        
    
    
