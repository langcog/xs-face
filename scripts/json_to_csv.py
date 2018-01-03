import os
import csv
import sys
import json

# should these go in common file?
OPENPOSE_DIR =  os.path.expandvars("$PI_HOME/openpose_output")
CSV_OUTPUT_DIR = os.path.expandvars("$HOME/xs-face/data")


if __name__ == "__main__":
    video = sys.argv[1]

    group = None
    name = None

    # change title of csv
    with open(os.path.join(CSV_OUTPUT_DIR, video)) as f:
        wr = csv.writer(f, "wb", quoting=csv.QUOTE_ALL)

    for root, dirs, filenames in os.walk(os.path.join(OPENPOSE_DIR, video)):
        for filename in filenames:

            frame = None

            with open(filename) as json_file:
                data = json.load(json_file)
                people = data["people"]

            if people:
                for person in people:
                    row = [group, name, frame] + \
                           person["pose_keypoints"] + \
                           person["face_keypoints"] + \
                           person["hand_left_keypoints"] + \
                           person["hand_right_keypoints"]
                    wr.writerow(row)
            else:
                wr.writerow([None]) # all 0s





