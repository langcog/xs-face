import os

DATA_DIR = "/volume1/Experiments/XS-FACE/final-set-materials/final-videos/headcam-final"
OUTPUT_DIR = "/var/services/homes/alessandro/xs-face/data/raw_ffmpeg_output"

if __name__ == "__main__":

    for root, subdirs, filenames in os.walk(DATA_DIR):
        for filename in filenames:
            if filename.endswith("objs.mov"):
                print("running ffmpeg on {}...".format(filename))
                full_filename = os.path.join(DATA_DIR, root, filename)
                os.system("ffmpeg -i {} &> {}/{}.output".format(full_filename, OUTPUT_DIR, filename))

