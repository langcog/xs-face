import os

DIR = "/volume1/Experiments/XS-FACE/final-set-materials/final-videos/headcam-final/"

if __name__ == "__main__":

    for root, subdirs, filenames in os.walk(DIR):
        for filename in filenames:
            if filename.endswith("objs.mov"):

                full_filename = os.path.join(DIR, root, filename)
                os.system("ffmpeg -i {0} &> ~/xs-face/data/raw_ffmpeg_output/{1}.output".format(full_filename, filename))

