import os
import csv

DIR = os.path.expandvars("$PI_HOME/frames3")
OUTPUT_FILE = os.path.expandvars("$HOME/xs-face/data/video_stats/extracted_frame_count.csv")

if __name__ == "__main__":
    with open(OUTPUT_FILE, 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(["video", "num_frames"])

        for d in os.listdir(DIR):
            num_frames = len(os.listdir(os.path.join(DIR, d)))
            wr.writerow([d, num_frames])
