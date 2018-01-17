import os
import csv
import ntpath

# TODO change folder name to sample or whatever in ~/xsface

BRIA_ANNOTATIONS = "/Users/alessandro/xsface/sample_hand_images"

if __name__ == "__main__":

    rows = {}

    for root, subdirectory, filenames in os.walk(BRIA_ANNOTATIONS):

        if root[len(root) - 1].isdigit(): # inside video directory
            for filename in filenames:
                if filename == ".DS_Store": continue
                video = ntpath.basename(root)
                group = str(int(video.split("_")[1][:2]))
                frame = filename.split(".")[0].split("-")[1]

                rows[video + filename.split(".")[0]] = [group, video, frame, "False", 0]

        elif ntpath.basename(root) == "annotations": # inside annotations
            video = ntpath.basename(os.path.dirname(root))
            for filename in filenames:
                arr = rows[video + filename.split(".")[0]]
                arr[3] = "True"
                rows[video + filename.split(".")[0]] = arr

    print(len(rows))

    with open("ground_truth_hands.csv", 'wb') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['group', 'video', 'frame', 'is_face', 'angle'])
        for key, val in rows.iteritems():
            wr.writerow(val)




