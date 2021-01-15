import os
import cv2
dirpath = r'/opt/amarnath/aicopia/idcard/idcardocr/train/crops/labels'
newdir = r'/opt/amarnath/aicopia/idcard/idcardocr/train/crops/trainformat'
# dict_info = {0: 'person', 1: 'half_person'}
dict_info = {0:'name', 1:'dl_number'} 

newdir = newdir+"/train.txt"
f1 = open(newdir, "w")
for fp in os.listdir(dirpath):
    if fp.endswith('.txt'):
        total_data = fp.replace(".txt",".jpg ")
        f = open(dirpath+"/"+fp, "r")
        lines = f.readlines()
        for line in lines:
            total_data += line.replace(" ", ',').replace('\n', ' ')
        total_data += "\n"
        f1.write('%s' % total_data)

f1.close()