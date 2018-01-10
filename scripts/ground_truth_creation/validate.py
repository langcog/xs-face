import os
import csv
import ntpath

# TODO change folder name to sample or whatever in ~/xsface

BRIA_ANNOTATIONS = "/Users/alessandro/Downloads/sample_images_bria"

if __name__ == "__main__":

    rows = {}

    for root, subdirectory, filenames in os.walk(BRIA_ANNOTATIONS):

        if root[len(root) - 1].isdigit(): # inside video directory
            for filename in filenames:
                if filename == ".DS_Store": continue
                group = ntpath.basename(os.path.dirname(root))
                video = ntpath.basename(root)
                frame = filename.split(".")[0].split("-")[1]

                rows[filename.split(".")[0]] = [group, video, frame, "False", 0]

        elif ntpath.basename(root) == "annotations": #inside annotations
            for filename in filenames:
                arr = rows[filename.split(".")[0]]
                arr[3] = "True"
                rows[filename.split(".")[0]] = arr

    print(len(rows))

    with open("ground_truth2.csv", 'wb') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['group', 'video', 'frame', 'is_face', 'angle'])
        for key, val in rows.iteritems():
            wr.writerow(val)




