import os
import cv2
dirpath = r'/opt/amarnath/aicopia/idcard/idcardocr/train/crops/labels'
imgdir = r'/opt/amarnath/aicopia/idcard/idcardocr/train/crops/dl_number'
newdir = r'/opt/amarnath/aicopia/idcard/idcardocr/train/crops/crops'
dict_info = {0:'0', 1:'1', 2:'2', 3:'3',4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9'} 


for k in dict_info:
    if os.path.isdir(newdir+"/"+dict_info[k]):
        files = os.listdir(newdir+"/"+dict_info[k])
        for f in files:
            os.remove(newdir+"/"+dict_info[k]+"/"+f)
    if not os.path.isdir(newdir+"/"+dict_info[k]):
        os.mkdir(newdir+"/"+dict_info[k])


 
# os.path.isdir(path)

# os.mkdir(path) 

for fp in os.listdir(dirpath):
    if fp.endswith('.txt'):
        imgpath = imgdir+"/"+fp.replace('.txt', '.jpg')
        f = open(dirpath+"/"+fp, "r")
        lines = f.readlines()
        image = cv2.imread(imgpath)
        h, w = image.shape[:2]
        cnt = 0
        for x in lines:
            s = x.split()
            label, x_center, y_center, wid, hei = s
                
            
            x_center = int(float(x_center)*w)
            y_center = int(float(y_center)*h)

            wid = int(float(wid)*w)
            hei = int(float(hei)*h)
            
            x_min = int(x_center - (wid/2))
            y_min = int(y_center - (hei/2))
            x_max = int(x_center + (wid/2))
            y_max = int(y_center + (hei/2))

            if x_min < 0:
                x_min = 0
            if y_min < 0:
                y_min = 0
            if x_max >= w:
                x_max = w-1
            if y_max >= h:
                y_max = h-1
            crop = image[y_min: y_max, x_min:x_max]
            print("crop", fp, crop)
            cv2.imshow("img1", cv2.pyrDown(crop))
            cv2.waitKey(1)
            newpath = fp.replace(".txt", '')
            newpath = newdir+"/"+dict_info[int(label)]+"/"+newpath+'_'+str(cnt)+".jpg"
            cv2.imwrite(newpath, crop)
            cnt += 1

        # print(f.read())