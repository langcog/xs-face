library(stringr)

######## MERGE IN EXACT TIMES FOR FRAMES #########
add.times <- function(x) {
  print(x$subid[1])
  ## from initial submission
  fname <- paste0("../../data/frame_times_redone/",
                 str_sub(as.character(x$subid[1]),start=4,end=8),
                 ".csv")
  
  if (file.exists(fname)) {
    times <- read_csv(fname)
    times$time <- times$best_time ## comes from show_frames python script
    x <- left_join(x, times)
    x$dt <- c(diff(x$time),.032) ## adds in 33ms for the last frame but otherwise goes on actual frame times, making an fps rate differences not a problem
  } else {
    print(paste0("**** ", x$subid[1], " is missing frames ****"))
    x$time <- NA
    x$dt <- NA
  }
  return(x)
}

######## ADD POSTURE CODING #########
add.posture <- function(x) {
  fname <- paste("../../data/posture/",
                 x$subid[1],
                 ".csv",
                 sep="")
  
  if (file.exists(fname)) {
    print(fname)
    postures <- read_csv(fname)
    postures <- postures[order(postures$start),] ## add line to sort by time in case weird coding order
   
    ## this reorders the postures so that they are "zeroed" relative to the beginning of the headcam videos
     postures <- regularize.postures(subset(postures,code=="posture"),x$subid[1]) ## needs subid to get real sync time later 
    x$posture <- factor(NA,levels=levels(postures$posture))
    x$orientation <- factor(NA,levels=levels(postures$orientation))
    
    # for each row of p, populate posture and orientation to x
    for (i in 1:nrow(postures)) {
      range <- x$time > postures$start[i] & x$time <= postures$end[i]
      x$posture[range] <- postures$posture[i]
      x$orientation[range] <- postures$orientation[i]
    }
  } else {
    print(paste0("**** ", x$subid[1], " is missing posture ****"))
    x$posture <- NA
    x$orientation <- NA
  }
  
  return(x)
}

add.posture.second <- function(x) {
  fname <- paste("../../data/posture/second/",
                 x$subid[1],
                 ".csv",
                 sep="")
  
  if (file.exists(fname)) {
    print(fname)
    postures <- read_csv(fname)
    postures <- postures[order(postures$start),] ## add line to sort by time in case weird coding order
    
    ## this reorders the postures so that they are "zeroed" relative to the beginning of the headcam videos
    postures <- regularize.postures(subset(postures,code=="posture"),x$subid[1]) ## needs subid to get real sync time later 
    x$posture_second <- factor(NA,levels=levels(postures$posture))
    x$orientation_second <- factor(NA,levels=levels(postures$orientation))
    
    # for each row of p, populate posture and orientation to x
    for (i in 1:nrow(postures)) {
      range <- x$time > postures$start[i] & x$time <= postures$end[i]
      x$posture_second[range] <- postures$posture[i]
      x$orientation_second[range] <- postures$orientation[i]
      print(paste0("**** ", x$subid[1], " has  second posture ****"))
      
    }
  } else {
    x$posture_second <- NA
    x$orientation_second <- NA
  }
  
  return(x)
}



get_sub_sync_time <- function(this_sub_id){
  sync_times_check_file <- read_csv("../../data/manual_sync_times/video_sync_times.csv") 
  s <- sync_times_check_file %>%
    filter(sid == this_sub_id) %>%
    mutate(sync_time_string =toString(sync_time_stamp)) %>%
    mutate(frames = str_split_fixed(sync_time_string,":",3)[,3]) %>%
    mutate(sec = str_split_fixed(sync_time_string,":",3)[,2]) %>%
    mutate(min = str_split_fixed(sync_time_string,":",3)[,1]) %>%
    mutate(sync_time_ms = as.numeric(min)*60000 + as.numeric(sec)*1000 + as.numeric(frames)*33.33)

  sync_time = s$sync_time_ms
  return(sync_time)
}


######## GET POSTURE CODING SORTED OUT #########
regularize.postures <- function (p,sub_id) {
  original.postures <- c("p","si","st","l","c","w","NIF")
  
  # clean up postures
  p$type <- factor(p$type,levels=original.postures)
  p$type <- plyr::revalue(p$type,c("p"="prone",
                   "si"="sit",
                   "st"="stand",
                   "l"="prone",
                   "c"="carry",
                   "w"="stand",
                   "NIF"="NIF"))
  p$type[p$type=="NIF"] <- NA
  p$posture <- p$type
  
  # clean up orientations
  p$orientation <- as.numeric(p$orient)
  p$orientation[is.nan(p$orientation)] <- NA
  
  p$orientation <- factor(p$orientation,levels=c(0,1,2,3,5))
  p$orientation <- plyr::revalue(p$orientation,
                      c("0"="far",
                        "1"="close",
                        "2"="close",
                        "3"="behind",
                        "5"="other"))
  

  
  
  # re-zero the times 
  # begin <- p$start[1] ### was doing this prior to march 2020; however noticed some files have some (small) discprencies
  ## with sync times outputted from finalcutpro; changed to this strategy to get more accurate codings
  # print(paste0("**** zero-time", begin, "*** min time:", min(p$start)))
  ## make sure that this value is the smallest that we're reading
  # assert_that(begin==min(p$start))
  
  
  # function above that reads in finalcutpro synctimes
  begin <- get_sub_sync_time(sub_id) 

  # subtract out sync_time and make into seconds (not milliseconds)
  p$start <- (p$start - begin)/1000
  p$end <- (p$stop - begin)/1000
  
  # set timestamp to 0 if we have coding from before the sync time (<0 means that it was before the headcam was synced with dv video)
  p$start[p$start<0]=0
  p$end[p$end<0]=0
  
  p <- p[,c("start","end","posture","orientation")]
  return(p)
}

######## GET NAMING CODING SORTED OUT #########
regularize.naming <- function (n) {
  words <- c("ball","car","brush","cat","tima","gimo","gasser","zem","manu")
  
  # replacements
  n$name[n$name == "truck"] <- "car"
  n$name[n$name == "kittycat"] <- "cat"
  n$name[n$name == "bobcat"] <- "cat"
  n$name <- factor(n$name, levels=words)
  
  n$familiarity <- "familiar"
  n$familiarity[n$name == "tima" |
    n$name == "gimo" |
    n$name == "gasser" |
    n$name == "zem" |
    n$name == "manu"] <- "novel"
  n$familiarity <- factor(n$familiarity)
  
  # make the times seconds since onset - # if excel output is HMS vs MS - ugh! this was causing a big bug in analyses prior to jan 2018
  n$time = as.character(n$time)
  timeBefore=n$time
  if (nchar(timeBefore[1])>8) { ## hacky but works.
    n$time=parse_date_time(timeBefore,"%H:%M:OS%")
  }
  else {
    n$time=parse_date_time(timeBefore,"%M:OS%")
  }
  assert_that(sum(hour(n$time))==0)  # check there are no hours! all sessions <20 minutes.
  n$time <- minute(n$time)*60+second(n$time) # convert to seconds

  n <- subset(n,!is.na(name))
  n$naming.instance <- naming.instance(n$name)
  return(n)
}



######## ADD NAMING INSTANCES #########
naming.instance <- function(ns) {
  ni <- rep(0,length(ns))

  for (l in levels(ns)) {
      this.name <- ns==l
      ni[this.name] <- cumsum(this.name)[this.name]
  }
  return(ni)
}

######## GET SUMMARY MEASURES OVER NAMINGS #########

get.namings <- function (x, window = c(-2,2), file_dir = '../../data/naming/') {  
  # read in naming times
  namings <- read.csv(paste(file_dir,
                            x$subid[1],
                            ".csv",
                            sep=""),
                      stringsAsFactors=FALSE)
  
  namings <- regularize.naming(namings)
}

get.namings.second <- function (x, window = c(-2,2), file_dir = '../../data/naming/second/') {
  # try for second file
  second_file = Sys.glob(paste(file_dir,x$subid[1], '*',".csv", sep=""))
  naming_second = read.csv(second_file)
  namings_second <- regularize.naming(naming_second)

}

summarize.naming <- function (x, window = c(-2,2), file_dir = '../../data/naming/') {  
  words <- c("ball","zem","car","manu","brush","gimo","tima","kittycat","bobcat","cat","gasser","puppy")

  # read in naming times
  namings <- read.csv(paste(file_dir,
                      x$subid[1],
                      ".csv",
                      sep=""),
                stringsAsFactors=FALSE)
  
  # print(x$subid[1])
  
  # rectify the coding
  namings <- regularize.naming(namings)
  
  # for each row of p, populate posture and orientation to x
  namings$posture <- factor(NA, levels=levels(x$posture))
  namings$orientation <- factor(NA, levels=levels(x$orientation))

  for (i in 1:nrow(namings)) {
    t <- namings$time[i]
    range <- c(max(c(0,t + window[1])),
               min(c(t+window[2],max(x$time,na.rm=T))))
    namings$detections[i] <- mean(x$detections[x$time > range[1] & x$time < range[2]], na.rm=TRUE)
    namings$posture[i] <- x$posture[(x$time > namings$time[i])][1]
    namings$orientation[i] <- x$orientation[(x$time > namings$time[i])][1]  
  }
  
  namings$age.grp <- x$age.grp[1]
  namings$age.at.test <- x$age.at.test[1]
  return(namings)
}
