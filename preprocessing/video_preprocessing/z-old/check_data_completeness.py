#!/usr/bin/python

## checks data completeness for all codings

import os, sys, re, csv, glob
from PyRTF import *

subs = []

with open("../data/demographics/demographics.csv", 'rU') as f:
    reader = csv.reader(f)
    next(reader, None)  # skip the headers
    for row in reader:
        subs.append(row[0])

# print subs
print "sub\tdets\tposture\tnaming\ttranscript"

for sub in subs:
    msg = sub + "\t"

    # check detectors
    if len(glob.glob("../data/detectors/*" + sub[3:10] + "*")) != 0:
        msg += "x"
        # print "x"

    msg += "\t"
               
    # check posture
    if len(glob.glob("../data/posture/raw/*" + sub + "*")) != 0:
        msg += "x"

    msg += "\t"
    
    # check namings
    if len(glob.glob("../data/naming/raw/*" + sub + "*")) != 0:
        msg += "x"

    msg += "\t"
    
    # check transcript
    if len(glob.glob("../data/naming/raw/*" + sub + "*")) != 0:
        msg += "x"

    print msg

