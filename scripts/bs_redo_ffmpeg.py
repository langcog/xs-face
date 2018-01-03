import os
import sys
import ntpath

OUTPUT_DIR = "/home/groups/mcfrank/frames/redo/"

videos = [
    "/home/groups/mcfrank/headcam_final/12-months/XS_1225_objs.mov",
    "/home/groups/mcfrank/headcam_final/12-months/XS_1222_objs.mov",
    "/home/groups/mcfrank/headcam_final/12-months/XS_1219_objs.mov",
    "/home/groups/mcfrank/headcam_final/12-months/XS_1224_objs.mov",
    "/home/groups/mcfrank/headcam_final/8-months/XS_0825_objs.mov",
    "/home/groups/mcfrank/headcam_final/8-months/XS_0822_objs.mov",
    "/home/groups/mcfrank/headcam_final/8-months/XS_0821_objs.mov",
    "/home/groups/mcfrank/headcam_final/8-months/XS_0819_objs.mov",
    "/home/groups/mcfrank/headcam_final/8-months/XS_0815_objs.mov",
    "/home/groups/mcfrank/headcam_final/16-months/XS_1604_objs.mov"
]

if __name__ == "__main__":
    video = videos[int(sys.argv[1]) - 1]

    dirname = '_'.join(ntpath.basename(video).split('_')[:2])

    os.system("mv /home/groups/mcfrank/frames/{} /home/groups/mcfrank/misc".format(dirname))

    cmd = 'ffmpeg -i {0} -vf "hflip,vflip,scale=720:480" -vsync 0 {1}/image-%5d.jpg' \
        .format(video, os.path.join(OUTPUT_DIR, dirname))

    os.system(cmd)