import os
import re
import sys
import csv
import ntpath
import traceback
import multiprocessing
sys.path.append('/home/sanchez7/local')
import cv2

OUTPUT_FILE = 'tmp/face_detection_%s.csv'


def detect_faces(gray_img):
    cascPath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    return faceCascade.detectMultiScale(
        gray_img,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )


def process_img(imgpath):
    # print('batch {0}: {1}%'.format(arg, i/1075.0 * 100))
    print imgpath
    gray_img = cv2.cvtColor(cv2.imread(imgpath), cv2.COLOR_BGR2GRAY)

    faces = detect_faces(gray_img)

    name = ntpath.basename(os.path.dirname(imgpath))
    group = str(int(name.split("_")[1][:2]))
    frame = re.search('image-(.*).jpg', ntpath.basename(imgpath)).group(1)

    rows = []

    if len(faces) == 0:
        rows.append([group, name, frame, False, None, None, None, None])
    else:
        for (x, y, w, h) in faces:
            rows.append([group, name, frame, True, x, y, w, h])


if __name__ == "__main__":
    vid_folder = sys.argv[1]
    vid = ntpath.basename(vid_folder)

    pool = multiprocessing.Pool()
    results = []

    for image in os.listdir(vid_folder):
        results.append(pool.apply_async(process_img, args=(os.path.join(vid_folder, image),)))

    pool.close()

    with open(OUTPUT_FILE % vid, 'wb') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        # wr.writerow(['group', 'video', 'frame', 'is_face', 'x', 'y', 'w', 'h'])

        for result in results:
            try:
                rows = result.get()
                for row in rows:
                    wr.writerow(row)
            except:
                traceback.print_exc()