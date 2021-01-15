from yolov4.tf import YOLOv4
import cv2
# yolo = YOLOv4()
yolo = YOLOv4(tiny=True)

yolo.classes = "/opt/amarnath/aicopia/idcard/idcardocr/label.names"
yolo.input_size = (320, 256)

yolo.make_model()
yolo.load_weights("/opt/amarnath/aicopia/idcard/idcardocr/weights/yolov4-tiny-30.weights", weights_type="yolo")
# yolo.load_weights("yolov4-tiny.weights", weights_type="yolo")

path = "/opt/amarnath/aicopia/idcard/idcardocr/train/images/14.jpg"
image = cv2.imread(path)
yolo.inference(media_path=path)

cv2.resize(image, (256, 320))
boxes = yolo.predict(image)
print(boxes)