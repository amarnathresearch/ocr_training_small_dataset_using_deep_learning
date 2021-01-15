# -*- coding: utf-8 -*-
"""amar_yolov4_tf_training.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VPj2r3oIJjRa3J9M_rbuNZkQGEdjtf3T
"""



from tensorflow.keras import callbacks, optimizers
from yolov4.tf import SaveWeightsCallback, YOLOv4
import time

yolo = YOLOv4(tiny=True)
yolo.classes = "/opt/amarnath/aicopia/idcard/idcardocr/label.names"
yolo.input_size = (320, 256) # == width, height
yolo.batch_size = 8

yolo.make_model()
# yolo.load_weights(
#     "/content/drive/My Drive/Hard_Soft/NN/yolov4/yolov4-tiny.conv.29",
#     weights_type="yolo"
# )


train_data_set = yolo.load_dataset(
    "/opt/amarnath/aicopia/idcard/idcardocr/train/train_format/train.txt",
    image_path_prefix="/opt/amarnath/aicopia/idcard/idcardocr/train/images",
    label_smoothing=0.05
)
val_data_set = yolo.load_dataset(
    "/opt/amarnath/aicopia/idcard/idcardocr/train/train_format/train.txt",
    image_path_prefix="/opt/amarnath/aicopia/idcard/idcardocr/train/images",
    training=False
)

# val_data_set

epochs = 400
lr = 1e-4

optimizer = optimizers.Adam(learning_rate=lr)
yolo.compile(optimizer=optimizer, loss_iou_type="ciou")

def lr_scheduler(epoch):
    if epoch < int(epochs * 0.5):
        return lr
    if epoch < int(epochs * 0.8):
        return lr * 0.5
    if epoch < int(epochs * 0.9):
        return lr * 0.1
    return lr * 0.01

_callbacks = [
    callbacks.LearningRateScheduler(lr_scheduler),
    callbacks.TerminateOnNaN(),
    callbacks.TensorBoard(
        log_dir="/opt/amarnath/aicopia/idcard/idcardocr/logs",
    ),
    SaveWeightsCallback(
        yolo=yolo, dir_path="/opt/amarnath/aicopia/idcard/idcardocr/weights",
        weights_type="yolo", epoch_per_save=10
    ),
]

yolo.fit(train_data_set,epochs=epochs,callbacks=_callbacks,validation_data=val_data_set,
    validation_steps=50,
    validation_freq=5,
    steps_per_epoch=100
)


