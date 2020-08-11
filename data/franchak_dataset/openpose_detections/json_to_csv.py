import os
import numpy as np
import pandas as pd

DATA_PATH = "/Users/brialong/Documents/GitHub/xs-face/data/franchak_dataset/openpose_detections/full_jsons/"
OUT_PATH = "/Users/brialong/Documents/GitHub/xs-face/data/franchak_dataset/openpose_detections/"


files = os.listdir(DATA_PATH)
full_df = [] 

for f in files:
	print f
	if not f.startswith('.'): 
		file_path = os.path.join(DATA_PATH, f)
		df = pd.read_json(file_path)
		df['subid'] = f
		this_sub=df[['subid','frame_num','face_openpose','hand_openpose','nose_conf','wrist_conf']]
		this_sub.to_csv(OUT_PATH + f + '_openpose.csv', index=False)

