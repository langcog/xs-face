import os
import re
import sys
import csv
import ntpath
import traceback
import multiprocessing

DATA_DIR = os.path.expandvars("$PI_HOME/frames")
OUTPUT_FILE = '../data/face_detection/face_detection.csv'

sys.path.append('/home/sanchez7/local')

import cv2


def detect_faces(gray_img):
    cascPath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    return faceCascade.detectMultiScale(
        gray_img,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )


def rotate_img(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result


def get_gray_img(img_path):
    img = cv2.imread(img_path)
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def process_img(root, filename):
    imgpath = os.path.join(root, filename)
    print imgpath
    gray_img = get_gray_img(imgpath)

    faces = detect_faces(gray_img)
    faces_rotated = detect_faces(rotate_img(gray_img, 180))

    group = ntpath.basename(os.path.dirname(root)).split('-')[0]
    name = '_'.join(ntpath.basename(root).split('_')[:2])
    frame_no = re.search('image-(.*).jpg', filename).group(1)


    rows = []

    face = False # TODO check if you can eval faces as bool
    for (x, y, w, h) in faces:
        face = True
        rows.append([group, name, frame_no, True, x, y, w, h, 0])

    if not face:
        rows.append([group, name, frame_no, False, None, None, None, None, 0])

    face = False
    for (x, y, w, h) in faces_rotated:
        face = True
        rows.append([group, name, frame_no, True, x, y, w, h, 180])

    if not face:
        rows.append([group, name, frame_no, False, None, None, None, None, 180])

    print rows
    return rows

if __name__ == "__main__": # 8-m/XS_0801/image-00004
    pool = multiprocessing.Pool()
    results = []
    for root, _, filenames in os.walk(DATA_DIR):
        print root
        for filename in filenames:
            results.append(pool.apply_async(process_img, args=(root, filename)))

    pool.close()

    f = open(OUTPUT_FILE, 'wb')
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow(['group', 'video', 'frame', 'is_face', 'x', 'y', 'w', 'h', 'angle'])

    for result in results:
        try:
            rows = result.get()
            print '***'
            print rows
            for row in rows:
                wr.writerow(row)
        except:
            traceback.print_exc()




