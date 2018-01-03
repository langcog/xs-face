import os
import csv

DATA_DIR = os.path.expandvars("$PI_HOME/frames")
OUTPUT_FILE = '../data/image_paths.csv'


if __name__ == "__main__":
    wr = csv.writer(open(OUTPUT_FILE, 'wb'), quoting=csv.QUOTE_ALL)

    for root, _, filenames in os.walk(DATA_DIR):
        for filename in filenames:
            wr.writerow([os.path.join(root, filename)])
