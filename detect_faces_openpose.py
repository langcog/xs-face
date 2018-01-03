import os
import re
import sys
import csv
import ntpath
import tensorflow as tf
from tf_pose_estimation.common import estimate_pose, CocoPart, read_imgfile
from tf_pose_estimation.networks import get_network
from scipy.ndimage import rotate

config = tf.ConfigProto()
config.gpu_options.allocator_type = 'BFC'
config.gpu_options.per_process_gpu_memory_fraction = 0.95
config.gpu_options.allow_growth = True

OUTPUT_FILE = 'data/face_detection/face_detection_%s.csv'
IMAGE_PATHS_FILE = 'data/image_paths.csv'


def process_images(imgpaths):

    input_height = 368
    input_width = 368
    model = "cmu"
    stage_level = 6

    input_node = tf.placeholder(tf.float32, shape=(1, input_height, input_width, 3), name='image')

    results = {}

    with tf.Session(config=config) as sess:
        net, _, last_layer = get_network(model, input_node, sess)

        for imgpath_arr in imgpaths:
            imgpath = imgpath_arr[0]
            image = rotate(read_imgfile(imgpath, input_width, input_height), 180)

            run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
            run_metadata = tf.RunMetadata()
            pafMat, heatMat = sess.run(
                [
                    net.get_output(name=last_layer.format(stage=stage_level, aux=1)),
                    net.get_output(name=last_layer.format(stage=stage_level, aux=2))
                ], feed_dict={'image:0': [image]}, options=run_options, run_metadata=run_metadata
            )
            heatMat, pafMat = heatMat[0], pafMat[0]
            humans = estimate_pose(heatMat, pafMat)
            results[imgpath] = humans

    return results


if __name__ == "__main__":
    img_index = int(sys.argv[1]) * 4171

    with open(IMAGE_PATHS_FILE, 'rb') as img_paths_f:
        img_paths = list(csv.reader(img_paths_f, delimiter=','))
        images_to_process = img_paths[img_index-4170:img_index+1]
        #images_to_process = img_paths[60*4170:60*4170 + 3]
        # images_to_process = [
        #     ["/share/PI/mcfrank/frames/8-months/XS_0801/image-01610.jpg"],
        #     ["/share/PI/mcfrank/frames/8-months/XS_0801/image-00002.jpg"],
        #     ["/share/PI/mcfrank/frames/8-months/XS_0801/image-00260.jpg"],
        #     #["/share/PI/mcfrank/frames/8-months/XS_0801/image-00038.jpg"]
        # ]

    # group video frame nose neck ... angle

    results = process_images(images_to_process)

    with open(OUTPUT_FILE % sys.argv[1], 'wb') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        # wr.writerow(['group', 'video', 'frame', 'is_face', 'x', 'y', 'w', 'h', 'angle'])

        for imgpath, humans in results.iteritems():

            group = ntpath.basename(os.path.dirname(os.path.dirname(imgpath))).split('-')[0]
            name = '_'.join(ntpath.basename(os.path.dirname(imgpath)).split('_')[:2])
            frame = re.search('image-(.*).jpg', ntpath.basename(imgpath)).group(1)

            if humans:
                for human in humans:
                    wr.writerow([group,
                                 name,
                                 frame,
                                 human[0][1] if human[0] else None, # Nose
                                 human[1][1] if human[1] else None, # Neck
                                 human[2][1] if human[2] else None, # RShoulder
                                 human[3][1] if human[3] else None, # RElbow
                                 human[4][1] if human[4] else None, # RWrist
                                 human[5][1] if human[5] else None, # LShoulder
                                 human[6][1] if human[6] else None, # LElbow
                                 human[7][1] if human[7] else None, # LWrist
                                 human[8][1] if human[8] else None, # RHip
                                 human[9][1] if human[9] else None, # RKnee
                                 human[10][1] if human[10] else None, # RAnkle
                                 human[11][1] if human[11] else None, # LHip
                                 human[12][1] if human[12] else None, # LKnee
                                 human[13][1] if human[13] else None, # LAnkle
                                 human[14][1] if human[14] else None, # REye
                                 human[15][1] if human[15] else None, # LEye
                                 human[16][1] if human[16] else None, # REar
                                 human[17][1] if human[17] else None, # LEar
                                 ])
            else:
                wr.writerow([group, name, frame] + [None for _ in range(18)])