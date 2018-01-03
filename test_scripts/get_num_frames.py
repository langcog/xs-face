import os
import csv


VIDEOS_DIR = os.path.expandvars("$PI_HOME/headcam_final")
CMD = "ffprobe -v error -count_frames -select_streams v:0   " \
      "-show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 {}"

if __name__ == "__main__":
    for video in os.listdir(VIDEOS_DIR):
        full_path = os.path.join(VIDEOS_DIR, video)
        os.system(CMD.format(full_path)) # capture output and put in CSV