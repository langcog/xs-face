import os
import sys

DATA_DIR = os.path.expandvars("$PI_HOME/headcam_final")
OUTPUT_DIR = os.path.expandvars("$PI_HOME/frames2")
FFMPEG_BIN = os.path.expandvars("$HOME/ffmpeg-3.4-64bit-static/ffmpeg")


if __name__ == "__main__":
    video_name = sys.argv[1]
    full_filename = os.path.join(DATA_DIR, video_name)
    video_dir_name = os.path.join(OUTPUT_DIR, '_'.join(video_name.split('_')[:2]))
    os.system('mkdir {0}'.format(video_dir_name))
    cmd = '{0} -i {1} -vf "hflip,vflip,scale=720:480" -vsync 0 {2}/image-%5d.jpg'\
        .format(FFMPEG_BIN, full_filename, video_dir_name)
    os.system(cmd)

