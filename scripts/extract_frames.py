import os
import ntpath
import traceback
import multiprocessing

DATA_DIR = os.path.expandvars("$PI_HOME/headcam_final")
OUTPUT_DIR = os.path.expandvars("$PI_HOME/frames")


if __name__ == "__main__":
    pool = multiprocessing.Pool()
    results = []
    for root, _, filenames in os.walk(DATA_DIR):
        for filename in filenames:
            full_filename = os.path.join(root, filename)
            video_dir_name = os.path.join(OUTPUT_DIR, ntpath.basename(root), '_'.join(filename.split('_')[:2]))
            os.system('mkdir -p {0}'.format(video_dir_name))
            cmd = 'ffmpeg -i {0} -vf "hflip,vflip,scale=720:480" -vsync 0 {1}/image-%5d.jpg'\
                .format(full_filename, video_dir_name)
            results.append(pool.apply_async(os.system, args=(cmd,)))
    pool.close()

    for result in results:
        try:
            result.get()
        except:
            traceback.print_exc()
