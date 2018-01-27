import os
os.system("module load opencv")
import cv2
import ntpath

# x, y, w, h

# m = {
# 	"09551":[120, 82, 279, 265],
# 	"07106":[217, 300, 338, 444],
# 	"10506":[441, 296, 692, 480]
# }

base = "/share/PI/mcfrank/frames_rotated/"
m2 = {
	base + "XS_0803/image-09551.jpg" : [120, 82, 279, 265],
	base + "XS_1222/image-07106.jpg" : [217, 300, 338, 444],
	base + "XS_1619/image-10506.jpg" : [441, 296, 692, 480]
}

if __name__ == "__main__":
	base = "/share/PI/mcfrank/"
	d = [base + "XS_0803/image-09551.jpg"]

	for k, v in m2.iteritems():
		image = cv2.imread(k)

		x, y, w, h = m2[k]

		cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

		cv2.imwrite(ntpath.basename(k).split(".")[0] + "_with_box.jpg", image)
