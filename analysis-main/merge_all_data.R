## main data merge script - prerequisite for all other analyses
rm(list=ls())
library(dplyr)
library(readr)
library(magrittr)
library(tidyr)
source("helper.R")

## load detectors, demo data, merge
dets <- read_csv("../data/final_output/mtcnn2.csv") %>%
  mutate(y = as.numeric(y)) # because of leading zeros, apparently
dets<-arrange(dets,video,frame) # comes out in weird order because of sherlock jobs!
dets$subid <- dets$video # common names
dets$frame<-as.numeric(dets$frame) # numeric
dets$face<-as.logical(dets$is_face) # make logical

demo.data <- read_csv("../data/demographics/demographics.csv") %>% 
  select(-ra, -assist, -len) ## -dot -dib fields did not exist, deleted bll
d <- dets %>%
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
  mutate(dt = 0, face = FALSE) %>%
  left_join(ages)

d <- bind_rows(d, complete_combos)

write_csv(d, "../data/consolidated_data.csv")

## Create a set of videos that passes the sanity checks in length_sanity_check.Rmd
d_passing <- filter(d, not(subid %in% c("XS_1205","XS_1211","XS_1225",
                                        "XS_1628","XS_1639")))

write_csv(d_passing, "../data/consolidated_data_passing.csv")
