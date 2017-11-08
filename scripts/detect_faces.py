import os
import re
import sys
import csv
import ntpath
import traceback
import multiprocessing
sys.path.append('/home/sanchez7/local')
import cv2

DATA_DIR = os.path.expandvars("$PI_HOME/frames")
OUTPUT_FILE = '../data/face_detection/face_detection_%s.csv'
IMAGE_PATHS_FILE = '../data/image_paths.csv'


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


def process_img(imgpath, i, arg):
    # print('batch {0}: {1}%'.format(arg, i/1075.0 * 100))
    print imgpath
    gray_img = cv2.cvtColor(cv2.imread(imgpath), cv2.COLOR_BGR2GRAY)

    faces = detect_faces(gray_img)
    faces_rotated = detect_faces(rotate_img(gray_img, 180))

    group = ntpath.basename(os.path.dirname(os.path.dirname(imgpath))).split('-')[0]
    name = '_'.join(ntpath.basename(os.path.dirname(imgpath)).split('_')[:2])
    frame = re.search('image-(.*).jpg', ntpath.basename(imgpath)).group(1)

    rows = []

    if len(faces) == 0:
        rows.append([group, name, frame, False, None, None, None, None, 0])
    else:
        for (x, y, w, h) in faces:
            rows.append([group, name, frame, True, x, y, w, h, 0])

    if len(faces_rotated) == 0:
        rows.append([group, name, frame, False, None, None, None, None, 180])
    else:
        for (x, y, w, h) in faces_rotated:
            rows.append([group, name, frame, True, x, y, w, h, 180])

    return rows


if __name__ == "__main__":
    img_index = int(sys.argv[1]) * 1075

    with open(IMAGE_PATHS_FILE, 'rb') as img_paths_f:
        img_paths = list(csv.reader(img_paths_f, delimiter=','))
        images_to_process = img_paths[img_index-1074:img_index+1]

    pool = multiprocessing.Pool()
    results = []

    for i, row in enumerate(images_to_process):
        results.append(pool.apply_async(process_img, args=(row[0], i, sys.argv[1])))

    pool.close()

    with open(OUTPUT_FILE % sys.argv[1], 'wb') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['group', 'video', 'frame', 'is_face', 'x', 'y', 'w', 'h', 'angle'])

        for result in results:
            try:
                rows = result.get()
                for row in rows:
                    wr.writerow(row)
            except:
                traceback.print_exc()
