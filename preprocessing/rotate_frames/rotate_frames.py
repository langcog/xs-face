# pip install Pillow if you don't already have it

# import image utilities
from PIL import Image

# import os / sys utilities
import os
import sys


DATA_DIR = os.path.expandvars("$PI_HOME/frames2")

# define a function that rotates images in the current directory
# given the rotation in degrees as a parameter
def rotateImages(folder):
    print(folder)
    # for each image in the current directory
    for image in os.listdir(os.path.join(DATA_DIR, folder)):
        # open the image
        img = Image.open(os.path.join(DATA_DIR, folder, image))
        # rotate and save the image with the same filename
        img.rotate(180).save(os.path.join(DATA_DIR, folder, image))
        print(image)
        # close the image
        img.close()


if __name__ == "__main__":
    rotateImages(sys.argv[1])

