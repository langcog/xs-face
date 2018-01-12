import os
import csv
import sys
import json
import ntpath

CSV_OUTPUT_DIR = os.path.expandvars("$HOME/xs-face/scripts/openpose/tmp")

# TODO 1229 is weird because title contains "cropped"
# TODO if no face or hand or whatever, fill in with 0s!!! first check if, and if not, extend with 0s

if __name__ == "__main__":
    video_full_path = sys.argv[1]
    video_filename = ntpath.basename(video_full_path)
    print(video_filename)

    subject = "_".join(video_filename.split("_")[:2])
    group = str(int(subject.split("_")[1][:2]))

    with open(os.path.join(CSV_OUTPUT_DIR, subject + ".csv"), "wb") as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)

        for filename in os.listdir(video_full_path):
            frame = filename.split("_")[3][7:]

            with open(os.path.join(video_full_path, filename), "rb") as json_file:
                data = json.load(json_file)
                people = data["people"]

            if people:
                for person in people:
                    row = [group, subject, frame] + \
                           person["pose_keypoints"] + \
                           person["face_keypoints"] + \
                           person["hand_left_keypoints"] + \
                           person["hand_right_keypoints"]
                    wr.writerow(row)
            else:
                wr.writerow([group, subject, frame] + [0 for _ in xrange(390)])






