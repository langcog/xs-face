import os
import csv
import ntpath
import xml.etree.ElementTree as ET

# TODO take in arg for wrist or face and change the corresponding is_face?

BRIA_ANNOTATIONS = "/Users/alessandro/Downloads/sample_hand_images_bll"

if __name__ == "__main__":

    rows = {}

    for root, subdirectory, filenames in os.walk(BRIA_ANNOTATIONS):

        if root[len(root) - 1].isdigit(): # inside video directory
            for filename in filenames:
                if filename == ".DS_Store": continue
                video = ntpath.basename(root)
                group = str(int(video.split("_")[1][:2]))
                frame = filename.split(".")[0].split("-")[1]

                rows[video + filename.split(".")[0]] = [group, video, frame, "False"]

        elif ntpath.basename(root) == "annotations": # inside annotations
            video = ntpath.basename(os.path.dirname(root))
            for filename in filenames:
                xmlroot = ET.parse(os.path.join(root, filename)).getroot()
                if xmlroot.findall("object"):
                    arr = rows[video + filename.split(".")[0]]
                    arr[3] = "True"
                    rows[video + filename.split(".")[0]] = arr

    print(len(rows))

    with open("ground_truth_wrists2.csv", 'wb') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['group', 'video', 'frame', 'is_face'])
        for key, val in rows.iteritems():
            wr.writerow(val)




