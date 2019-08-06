"""
Retrain the YOLO model for your own dataset.
"""

import numpy as np
import json
import datetime
import os
import multiprocessing
import random
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID" # so the IDs match nvidia-smi
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1" # "0, 1" for multiple

import keras.backend as K
import tensorflow as tf
import keras
from keras.layers import Input, Lambda
from keras.models import Model
from keras.optimizers import Adam
from keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
K.set_session(session)

from yolo3.model import preprocess_true_boxes, yolo_body, tiny_yolo_body, yolo_loss
from yolo3.utils import mc3_get_random_data,get_random_data_own

class LRTensorBoard(TensorBoard):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_epoch_end(self, epoch, logs=None):
        logs.update({'lr': K.eval(self.model.optimizer.lr)})
        super().on_epoch_end(epoch, logs)


def _main():
    # adam, momentum or nesterov
    opt_string_1 = "adam"
    opt_string_2 = "adam"

    LEARNING_RATE = 0.001
    #using in lr decay
    LR_DECAY = 0.95
    #using in momentum and nesterov
    MOMENTUM = 0.9
    #using in adam
    ADAM_BETA_1 = 0.9
    ADAM_BETA_2 = 0.99
    
    BATCH_SIZE = 30
    
    IS_SAVE = True
    
    input_shape = (480,640) # multiple of 32, hw
    
    im_dir = '/data/mc_data/images_12k'
    train_json_path = '../annotations/MC3_train.json'
    val_json_path = '../annotations/MC3_val.json'
    classes_path = 'model_data/mc3_classes.txt'
    anchors_path = 'model_data/yolo_anchors.txt'
#     weights_path = 'model_data/darknet53.h5'
    weights_path = 'logs/20180726T1927_adam-adam/ep045-loss13.949-val_loss14.902.h5'
    base_dir = './logs'
    
    f = open(train_json_path,'r')
    train_info = json.load(f)
    f.close()
    f = open(val_json_path,'r')
    val_info = json.load(f)
    f.close()
    
    train_num = len(train_info)
    val_num = len(val_info)
    
    now = datetime.datetime.now()
    log_dir = os.path.join(base_dir,"{:%Y%m%dT%H%M}_".format(now)+opt_string_1+"-"+opt_string_2)
#     log_dir = os.path.join(base_dir,"{:%Y%m%dT%H%M}_".format(now)+opt_string)
    
    class_names = get_classes(classes_path)
    num_classes = len(class_names)
    anchors = get_anchors(anchors_path)
    
    model = create_model(input_shape, anchors, num_classes,
            freeze_body=2, weights_path=weights_path)
    
#     is_tiny_version = len(anchors)==6 # default setting
#     if is_tiny_version:
#         model = create_tiny_model(input_shape, anchors, num_classes,
#             freeze_body=2, weights_path=weights_path)
#     else:
#         model = create_model(input_shape, anchors, num_classes,
#             freeze_body=2, weights_path=weights_path) # make sure you know what you freeze

    logging = LRTensorBoard(log_dir=log_dir)
    checkpoint = ModelCheckpoint(os.path.join(log_dir,'ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5'),
                                monitor='val_loss',
                                 save_weights_only=True, save_best_only=True, period=3)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=3, verbose=1)
    if IS_SAVE:
        callbacks = [logging, checkpoint,reduce_lr]
    else:
        callbacks = [reduce_lr]
    #early_stopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=1)
    
    if opt_string_1 == "momentum":
        opt = keras.optimizers.SGD(lr=LEARNING_RATE,momentum=MOMENTUM)
    if opt_string_1 == "nesterov":
        opt = keras.optimizers.SGD(lr=LEARNING_RATE,momentum=MOMENTUM,nesterov=True)
    if opt_string_1 == "adam":
        opt = keras.optimizers.Adam(lr=LEARNING_RATE,beta_1=ADAM_BETA_1,
                                    beta_2=ADAM_BETA_2)
    
    train_generator = mysequence(im_dir,train_info, BATCH_SIZE, input_shape, anchors, num_classes)
    val_generator = mysequence(im_dir,val_info, BATCH_SIZE, input_shape, anchors, num_classes)
    
    # Train with frozen layers first, to get a stable loss.
    # Adjust num epochs to your dataset. This step is enough to obtain a not bad model.
    if True:
        model.compile(optimizer=opt, loss={
            # use custom yolo_loss Lambda layer.
            'yolo_loss': lambda y_true, y_pred: y_pred})

        print('Train on {} samples, val on {} samples, with batch size {}.'.format(train_num, val_num, BATCH_SIZE))
        model.fit_generator(train_generator,
#                 steps_per_epoch=1,
                  steps_per_epoch=max(1, train_num//BATCH_SIZE),
                validation_data=val_generator,
                validation_steps=max(1, val_num//BATCH_SIZE),
                epochs=50,
                initial_epoch=0,
                callbacks=callbacks,
                workers = 7,
#                 workers = multiprocessing.cpu_count(),
                max_queue_size = 10,
                use_multiprocessing = True
                           )
        model.save_weights(os.path.join(log_dir, 'trained_weights_stage_1.h5'))
    
    BATCH_SIZE = 5
    train_generator = mysequence(im_dir,train_info, BATCH_SIZE, input_shape, anchors, num_classes)
    val_generator = mysequence(im_dir,val_info, BATCH_SIZE, input_shape, anchors, num_classes)
    
    if opt_string_2 == "momentum":
        opt = keras.optimizers.SGD(lr=LEARNING_RATE,momentum=MOMENTUM)
    if opt_string_2 == "nesterov":
        opt = keras.optimizers.SGD(lr=LEARNING_RATE,momentum=MOMENTUM,nesterov=True)
    if opt_string_2 == "adam":
        opt = keras.optimizers.Adam(lr=LEARNING_RATE,beta_1=ADAM_BETA_1,
                                    beta_2=ADAM_BETA_2)
    # Unfreeze and continue training, to fine-tune.
    # Train longer if the result is not good.
    if True:
        for i in range(len(model.layers)):
            model.layers[i].trainable = True
        model.compile(optimizer=opt, loss={'yolo_loss': lambda y_true, y_pred: y_pred}) # recompile to apply the change
        print('Unfreeze all of the layers.')

        print('Train on {} samples, val on {} samples, with batch size {}.'.format(train_num, val_num, BATCH_SIZE))
        model.fit_generator(train_generator,
            steps_per_epoch=max(1, train_num//BATCH_SIZE),
            validation_data=val_generator,
            validation_steps=max(1, val_num//BATCH_SIZE),
            epochs=100,
            initial_epoch=50,
            callbacks=callbacks,
            workers = 7,
#             workers = multiprocessing.cpu_count(),
            max_queue_size = 10,
            use_multiprocessing = True
                           )
        model.save_weights(os.path.join(log_dir, 'trained_weights_final.h5'))

    # Further training if needed.


def get_classes(classes_path):
    '''loads the classes'''
    with open(classes_path) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names

def get_anchors(anchors_path):
    '''loads the anchors from a file'''
    with open(anchors_path) as f:
        anchors = f.readline()
    anchors = [float(x) for x in anchors.split(',')]
    return np.array(anchors).reshape(-1, 2)


def create_model(input_shape, anchors, num_classes, load_pretrained=True, freeze_body=2,
            weights_path='model_data/darknet53.h5'):
    '''create the training model'''
    K.clear_session() # get a new session
    image_input = Input(shape=(None, None, 3))
    h, w = input_shape
    num_anchors = len(anchors)

    y_true = [Input(shape=(h//{0:32, 1:16, 2:8}[l], w//{0:32, 1:16, 2:8}[l], \
        num_anchors//3, num_classes+5)) for l in range(3)]

    model_body = yolo_body(image_input, num_anchors//3, num_classes)
    print('Create YOLOv3 model with {} anchors and {} classes.'.format(num_anchors, num_classes))

    if load_pretrained:
        model_body.load_weights(weights_path, by_name=True)
        print('Load weights {}.'.format(weights_path))
        if freeze_body in [1, 2]:
            # Freeze darknet53 body or freeze all but 3 output layers.
            num = (185, len(model_body.layers)-3)[freeze_body-1]
            for i in range(num): model_body.layers[i].trainable = False
            print('Freeze the first {} layers of total {} layers.'.format(num, len(model_body.layers)))

    model_loss = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss',
        arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.5})(
        [*model_body.output, *y_true])
    model = Model(inputs=[model_body.input, *y_true], outputs=model_loss)

    return model

# def create_tiny_model(input_shape, anchors, num_classes, load_pretrained=True, freeze_body=2,
#             weights_path='model_data/darknet53.h5'):
#     '''create the training model, for Tiny YOLOv3'''
#     K.clear_session() # get a new session
#     image_input = Input(shape=(None, None, 3))
#     h, w = input_shape
#     num_anchors = len(anchors)

#     y_true = [Input(shape=(h//{0:32, 1:16}[l], w//{0:32, 1:16}[l], \
#         num_anchors//2, num_classes+5)) for l in range(2)]

#     model_body = tiny_yolo_body(image_input, num_anchors//2, num_classes)
#     print('Create Tiny YOLOv3 model with {} anchors and {} classes.'.format(num_anchors, num_classes))

#     if load_pretrained:
#         model_body.load_weights(weights_path, by_name=True)
#         print('Load weights {}.'.format(weights_path))
#         if freeze_body in [1, 2]:
#             # Freeze the darknet body or freeze all but 2 output layers.
#             num = (20, len(model_body.layers)-2)[freeze_body-1]
#             for i in range(num): model_body.layers[i].trainable = False
#             print('Freeze the first {} layers of total {} layers.'.format(num, len(model_body.layers)))

#     model_loss = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss',
#         arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.7})(
#         [*model_body.output, *y_true])
#     model = Model(inputs=[model_body.input, *y_true], outputs=model_loss)

#     return model

# def data_generator(im_dir,annotation_info,batch_size,input_shape,anchors,num_classes):
#     ann_info = annotation_info
#     index = 0
#     n = len(ann_info)
#     while True:
#         image_data = []
#         box_data = []
#         for i in range(batch_size):
#             if index==0:
#                 np.random.shuffle(ann_info)
#             info = ann_info[index]
#             image, box = mc3_get_random_data(im_dir,info,input_shape)
#             image_data.append(image)
#             box_data.append(box)
#             index = (index+1) % n
#         image_data = np.array(image_data)
#         box_data = np.array(box_data)
#         y_true = preprocess_true_boxes(box_data, input_shape, anchors, num_classes)
#         yield [image_data, *y_true], np.zeros(batch_size)

# def data_generator_wrapper(im_dir,annotation_info,batch_size, input_shape, anchors, num_classes):
#     n = len(annotation_info)
#     if n==0 or batch_size<=0: return None
# #     return data_generator(im_dir,annotation_info, batch_size, input_shape, anchors, num_classes)
#     return mysequence(im_dir,annotation_info, batch_size, input_shape, anchors, num_classes)

class mysequence(keras.utils.Sequence):
    def __init__(self, im_dir,annotation_info,batch_size,input_shape,anchors,num_classes):
        self.batch_size = batch_size
        self.im_dir = im_dir
        self.info = annotation_info
        self.input_shape = input_shape
        self.anchors = anchors
        self.num_classes = num_classes
    
    def __len__(self):
        return int(len(self.info) / self.batch_size) # the length is the number of batches
    
    def on_epoch_end(self):
        random.shuffle(self.info)
    
    def __getitem__(self, batch_id):
        image_data = []
        box_data = []
        for i in range(batch_id * self.batch_size, (batch_id+1) * self.batch_size):
            n = len(self.info)
            index = int(i % n)
            info = self.info[index]
#             image, box = mc3_get_random_data(self.im_dir,info,self.input_shape)
            image, box = get_random_data_own(self.im_dir,info,self.input_shape)
            #print(box)
            image_data.append(image)
            box_data.append(box)
        image_data = np.array(image_data)
        box_data = np.array(box_data)
        y_true = preprocess_true_boxes(box_data, self.input_shape, self.anchors, self.num_classes)
        return [image_data, *y_true], np.zeros(self.batch_size)

if __name__ == '__main__':
    _main()
