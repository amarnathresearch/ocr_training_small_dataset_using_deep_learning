import os
import xml.etree.ElementTree as ET

dirpath = r'/opt/amarnath/aicopia/idcard/idcardocr/train/crops/dl_number'  # The directory where the xml file was originally stored
newdir = r'/opt/amarnath/aicopia/idcard/idcardocr/train/crops/labels'  # The txt directory formed after modifying the label

if not os.path.exists(newdir):
    os.makedirs(newdir)

for fil in os.listdir(newdir):
    print("removing existing repository", newdir+"/"+fil)
    os.remove(newdir+"/"+fil)

# -*- coding: utf-8 -*-

from xml.dom import minidom
import os
import glob

lut={}
lut["0"] =0
lut["1"] =1
lut["2"] =2
lut["3"] =3
lut["4"] =4
lut["5"] =5
lut["6"] =6
lut["7"] =7
lut["8"] =8
lut["9"] =9



def convert_coordinates(size, box):
    dw = 1.0/size[0]
    dh = 1.0/size[1]
    x = (box[0]+box[1])/2.0
    y = (box[2]+box[3])/2.0
    w = box[1]-box[0]
    h = box[3]-box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


def convert_xml2yolo( lut ):

    for fname in glob.glob(dirpath+"/*.xml"):
        
        xmldoc = minidom.parse(fname)
        
        fname_out = newdir+"/"+fname.split("/")[-1].replace('.xml','.txt')
        print("fname_out", fname_out)
        with open(fname_out, "w") as f:

            itemlist = xmldoc.getElementsByTagName('object')
            size = xmldoc.getElementsByTagName('size')[0]
            width = int((size.getElementsByTagName('width')[0]).firstChild.data)
            height = int((size.getElementsByTagName('height')[0]).firstChild.data)

            for item in itemlist:
                # get class label
                classid =  (item.getElementsByTagName('name')[0]).firstChild.data
                if classid in lut:
                    label_str = str(lut[classid])
                else:
                    label_str = "-1"
                    print ("warning: label '%s' not in look-up table" % classid)
                if label_str != "-1":
                    # get bbox coordinates
                    xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
                    ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
                    xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
                    ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data
                    b = (float(xmin), float(xmax), float(ymin), float(ymax))
                    bb = convert_coordinates((width,height), b)
                    #print(bb)

                    f.write(label_str + " " + " ".join([("%.6f" % a) for a in bb]) + '\n')

        print ("wrote %s" % fname_out)



def main():
    convert_xml2yolo( lut )


if __name__ == '__main__':
    main()