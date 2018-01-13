## main data merge script - prerequisite for all other analyses
rm(list=ls())
library(dplyr)
library(readr)
library(magrittr)
library(tidyr)
library(assertthat)
source("helper.R")

## load detectors for mtcnn2
dets <- read_csv("../data/final_output/mtcnn3.csv") %>%
  mutate(subid = video) %>%
  mutate(frame = as.numeric(frame)) %>%
  mutate(faceMT = as.logical(is_face)) %>%
  distinct(video,frame,.keep_all=TRUE)   

# open pose detectors
detsOpenPose <- read_csv("../data/final_output/openpose_results_truncated_2.csv") 
detsOpenPose <- detsOpenPose %>%
  mutate(video = name) %>%
  distinct(video,frame,.keep_all=TRUE)  %>%
  mutate(frame = as.numeric(frame)) %>%
  mutate(faceOP = Nose_conf!=0 & REye_conf!=0 | LEye_conf!=0 )  %>%
  mutate(handOP = LWrist_conf!=0 | RWrist_conf!=0 )   
  
# viola jones detectors
detsViola <- read_csv("../data/final_output/viola.csv") 
detsViola <- detsViola %>%
  distinct(video,frame,.keep_all=TRUE)  %>%
  mutate(faceVJ = as.logical(is_face))  %>%
  mutate(frame = as.numeric(frame)) 

# merge all three detectors
alldets=left_join(dets,detsViola[,c("video","frame","faceVJ")]) 
alldets=left_join(alldets,detsOpenPose[,c("video","frame","faceOP","handOP")]) 

# load demographics and pose / orientation / timing
demo.data <- read_csv("../data/demographics/demographics.csv") %>% 
  select(-ra, -assist, -len) ## -dot -dib fields did not exist, deleted bll

# rearrange so we make sure it is in the order of the frames
alldets<-arrange(alldets,video,frame) 

## OpenPose doesn't get all frames. Let's check out the frames it deleted somehow.
missingInd=is.na(alldets$faceOP)
assert_that(sum(is.na(alldets$faceOP))==57)

missingOP<-alldets %>% 
  filter(missingInd) 

# None of the missing frames are faces. Replace OP "NAN" detections with "FALSE"
alldets$faceOP[missingInd]=FALSE
alldets$handOP[missingInd]=FALSE

# calls helper functions in helper.r to get times and posture coding integrated
d <- alldets %>%
  distinct(video,frame,.keep_all=TRUE)  %>%
  select(-c(is_face,video)) %>% # redudant with faceMT & subid, dropping
  left_join(demo.data) %>%
  group_by(subid) %>%
  do(add.times(.)) %>% 
  group_by(subid) %>%
  do(add.posture(.))

# Complete the data frame so that zeros get counted: expands so that each subid
# includes a zero length row for each posture and orientation.
# this was annoying.

ages <- d %>%
  group_by(subid) %>%
  summarise(age.grp = mean(age.grp)) 

complete_combos <- expand(d, nesting(posture, orientation), 
                          subid) %>% 
  mutate(dt = 0, faceMT = FALSE, faceVJ = FALSE, faceOP = FALSE, handOP = FALSE) %>%
  left_join(ages)

d <- bind_rows(d, complete_combos)

## save it out
write_csv(d, "../data/consolidateddata/consolidated_data_3dets.csv")

