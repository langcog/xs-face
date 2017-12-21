import os
import re
import sys
import csv
import cv2
import face
import ntpath
import traceback
import multiprocessing
from scipy import misc
from scipy.ndimage import rotate

DATA_DIR = os.path.expandvars("$PI_HOME/frames")
OUTPUT_FILE = '../data/face_detection/face_detection_%s.csv'
IMAGE_PATHS_FILE = '../data/image_paths.csv'


def process_img(imgpath):
    print imgpath
    img = misc.imread(imgpath)
    detector = face.Detection()

    faces = detector.find_faces(img)
    faces_rotated = detector.find_faces(rotate(img, 180))

    group = ntpath.basename(os.path.dirname(os.path.dirname(imgpath))).split('-')[0]
    name = '_'.join(ntpath.basename(os.path.dirname(imgpath)).split('_')[:2])
    frame = re.search('image-(.*).jpg', ntpath.basename(imgpath)).group(1)

    rows = []

    if len(faces) == 0:
        rows.append([group, name, frame, False, None, None, None, None, 180])
    else:
        for f in faces:
            arr = f.bounding_box
            x, y, w, h = arr[0], arr[1], arr[2], arr[3]
            rows.append([group, name, frame, True, x, y, w, h, 180])

    if len(faces_rotated) == 0:
        rows.append([group, name, frame, False, None, None, None, None, 0])
    else:
        for f in faces_rotated:
            arr = f.bounding_box
            x, y, w, h = arr[0], arr[1], arr[2], arr[3]
            rows.append([group, name, frame, True, x, y, w, h, 0])

    return rows


if __name__ == "__main__":
    img_index = int(sys.argv[1]) * 4171

    with open(IMAGE_PATHS_FILE, 'rb') as img_paths_f:
        img_paths = list(csv.reader(img_paths_f, delimiter=','))
        images_to_process = img_paths[img_index-4170:img_index+1]
        #images_to_process = img_paths[60*4170:60*4170 + 15]
        # images_to_process = [
        #     ["/share/PI/mcfrank/frames/8-months/XS_0801/image-00247.jpg"],
        #     ["/share/PI/mcfrank/frames/8-months/XS_0801/image-00250.jpg"],
        #     ["/share/PI/mcfrank/frames/8-months/XS_0801/image-00260.jpg"],
        #     #["/share/PI/mcfrank/frames/8-months/XS_0801/image-00038.jpg"]
        # ]

    pool = multiprocessing.Pool()
    results = []

    for row in images_to_process:
        results.append(pool.apply_async(process_img, args=(row[0],)))

    pool.close()

    with open(OUTPUT_FILE % sys.argv[1], 'wb') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        # wr.writerow(['group', 'video', 'frame', 'is_face', 'x', 'y', 'w', 'h', 'angle'])

        for result in results:
            try:
                rows = result.get()
                for row in rows:
                    wr.writerow(row)
            except:
                traceback.print_exc()
