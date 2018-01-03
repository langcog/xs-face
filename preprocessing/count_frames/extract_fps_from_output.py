import os
import re
import csv

OUTPUT_DIR = "/var/services/homes/alessandro/xs-face/data/raw_ffmpeg_output"
CSV_FILE = "/var/services/homes/alessandro/xs-face/data/new_movie_lengths.csv"


def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def get_num_frames(ffmpeg_output):
    right_ind = ffmpeg_output.index("fps")
    left_ind = ffmpeg_output[:right_ind].rfind(",")
    return float(ffmpeg_output[left_ind+1:right_ind])

if __name__ == "__main__":

    movie_lengths_f = open(CSV_FILE, 'wb')
    wr = csv.writer(movie_lengths_f, quoting=csv.QUOTE_ALL)
    wr.writerow(["subid", "fps", "length"])

    for filename in os.listdir(OUTPUT_DIR):
        with open(os.path.join(OUTPUT_DIR, filename), 'r') as ffmpeg_output_f:
            ffmpeg_output = ffmpeg_output_f.read()

        subid = filename.split("_objs")[0]
        num_frames = get_num_frames(ffmpeg_output)
        length = get_sec(re.findall(r'Duration: ([^]]*)\, start', ffmpeg_output)[0])

        wr.writerow([subid, num_frames, length])


