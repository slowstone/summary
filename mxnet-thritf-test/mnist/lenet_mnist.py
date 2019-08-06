#!/usr/bin/env python
# coding: utf-8

# # lenet_mnist

# In[12]:


import mxnet as mx
import os
import struct
import numpy as np
import logging
import random

# In[13]:


def load_mnist(path, kind='train'):
    """Load MNIST data from `path`"""
    labels_path = os.path.join(path,'{}-labels-idx1-ubyte'.format(kind))
    images_path = os.path.join(path,'{}-images-idx3-ubyte'.format(kind))
    with open(labels_path, 'rb') as lbpath:
        magic, n = struct.unpack('>II',
                                 lbpath.read(8))
        labels = np.fromfile(lbpath,
                             dtype=np.uint8).reshape(n)

    with open(images_path, 'rb') as imgpath:
        magic, num, rows, cols = struct.unpack('>IIII',
                                               imgpath.read(16))
        images = np.fromfile(imgpath,
                             dtype=np.uint8).reshape((num,1,rows,cols))
    print(kind)
    print("label num:",n)
    print("image num:",num)
    print("image rows:",rows)
    print("image cols:",cols)
    images = images/255
    return images, labels

'''
conv(5,5,32) relu avg_pool
conv(5,5,64) relu avg_pool
fc 1024 relu
fc 10 softmax
'''
def lenet5(data):
    C1 = mx.sym.Convolution(data=data,kernel=(5,5),num_filter=32,name='C1')
    C1 = mx.sym.Activation(data=C1,act_type='relu',name='C1_relu')
    S2 = mx.sym.Pooling(data=C1,kernel=(2,2),pool_type='avg',stride=(2,2),name='S2')
    C3 = mx.sym.Convolution(data=S2,kernel=(5,5),num_filter=64,name='C3')
    C3 = mx.sym.Activation(data=C3,act_type='relu',name='C3_relu')
    S4 = mx.sym.Pooling(data=C3,kernel=(2,2),pool_type='avg',stride=(2,2),name='S4')
    F5 = mx.sym.FullyConnected(data=S4,num_hidden=1024,name='F5')
    F5 = mx.sym.Activation(data=F5,act_type='relu',name='F5_relu')
    F6 = mx.sym.FullyConnected(data=F5,num_hidden=10,name='F6')
    output = mx.sym.SoftmaxOutput(data=F6,name='softmax')
    return output

if __name__ == '__main__':

    # In[15]:
    
    logging.getLogger().setLevel(logging.INFO)
    
    # super param
    BACH_SIZE = 500
    LEARNING_RATE = 0.1
    MOMENTUM = 0.9
    LR_FACTOR = 0.1
    LR_SCHRDULER_STEPS = 300
    GPUS = [2,3]
    IS_SAVE = False
    
    if IS_SAVE:
        CHECKPOINT_DIR = './logs'
        if not os.path.exists(CHECKPOINT_DIR):
            os.makedirs(CHECKPOINT_DIR)
        import datetime
        now = datetime.datetime.now()
        CHECKPOINT_DIR = os.path.join(CHECKPOINT_DIR,"{:%Y%m%dT%H%M}".format(now))
        if not os.path.exists(CHECKPOINT_DIR):
            os.makedirs(CHECKPOINT_DIR)
        CHECKPOINT_PATH = os.path.join(CHECKPOINT_DIR,"lenet5-mnist")
    
    #load_mnist
    train_im,train_la = load_mnist('/mnt/cephfs/lab/xuyan.bupt/dataset/mnist','train')
    val_im,val_la = load_mnist('/mnt/cephfs/lab/xuyan.bupt/dataset/mnist','t10k')
    
    #data iter
    train_iter = mx.io.NDArrayIter(data=train_im,
                                   label=train_la,
                                   batch_size=BACH_SIZE,
                                   data_name='im_data',
                                   label_name='softmax_label')
    val_iter = mx.io.NDArrayIter(data=val_im,
                                 label=val_la,
                                 batch_size=BACH_SIZE,
                                data_name='im_data',
                                   label_name='softmax_label')
    
    if len(GPUS) == 0:
        devs = mx.cpu()
    else:
        devs = [mx.gpu(i) for i in GPUS]
    
    #network build
    im_data = mx.sym.Variable(name='im_data')
    net = lenet5(im_data)
    mod = mx.mod.Module(symbol=net,
                        context=devs,
                        data_names=['im_data'],
                        label_names=['softmax_label'])

    #set opt
    lr_scheduler = mx.lr_scheduler.FactorScheduler(step=LR_SCHRDULER_STEPS, factor=LR_FACTOR)
    optimizer_params = {
                    'learning_rate': LEARNING_RATE,
                    'wd': 0.0005,
                    'lr_scheduler': lr_scheduler,
                    'momentum': MOMENTUM
                    }
    
    #init
    initializer = mx.init.Xavier(
       rnd_type='gaussian', factor_type='in', magnitude=2)
    
    
    #callbacks
    batch_callbacks = [
            mx.callback.Speedometer(BACH_SIZE, 10)
#             mx.callback.ProgressBar(total=10)
#             mx.callback.LogValidationMetricsCallback()
#             mx.callback.log_train_metric(10)
    ]
    if IS_SAVE:
        epoch_callbacks = [
            mx.callback.do_checkpoint(CHECKPOINT_PATH, 1)
        ] 
    else:
        epoch_callbacks = None

    #train
    mod.fit(train_iter,
            eval_data=val_iter,
            optimizer='sgd',
            optimizer_params=optimizer_params,
            batch_end_callback=batch_callbacks,
            epoch_end_callback=epoch_callbacks,
            initializer = initializer,
            eval_metric='acc',
            num_epoch=8)
