"""Miscellaneous utility functions."""

from functools import reduce

from PIL import Image
import numpy as np
import os
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb

def compose(*funcs):
    """Compose arbitrarily many functions, evaluated left to right.

    Reference: https://mathieularose.com/function-composition-in-python/
    """
    # return lambda x: reduce(lambda v, f: f(v), funcs, x)
    if funcs:
        return reduce(lambda f, g: lambda *a, **kw: g(f(*a, **kw)), funcs)
    else:
        raise ValueError('Composition of empty sequence not supported.')

def MC3_letterbox_image(image, size):
    '''resize image with unchanged aspect ratio using padding'''
    iw, ih = image.size[:2]
    h, w = size
    if iw/ih > w/h:
        nw = w
        nh = int(nw/iw * ih)
    else:
        nh = h
        nw = int(nh/ih * iw)

    new_image = image.resize((nw,nh), Image.BICUBIC)
    pad_image = Image.new('RGB', (w,h), (0,0,0))
    pad_image.paste(new_image, (0,0))
    pad_image = np.array(pad_image,dtype='float64')
#     pad_image = pad_image/255
    return pad_image

def letterbox_image(image, size):
    '''resize image with unchanged aspect ratio using padding'''
    iw, ih = image.size
    h, w = size
    scale = min(w/iw, h/ih)
    nw = int(iw*scale)
    nh = int(ih*scale)

    image = image.resize((nw,nh), Image.BICUBIC)
    new_image = Image.new('RGB', size, (0,0,0))
    new_image.paste(image, ((w-nw)//2, (h-nh)//2))
#     new_image.paste(image, (0,0))
    return new_image

def rand(a=0, b=1):
    return np.random.rand()*(b-a) + a

def get_random_data_own(im_dir,info, input_shape, max_boxes=5, jitter=.3, hue=.1, sat=1.5, val=1.5, proc_img=True):
    '''random preprocessing for real-time data augmentation'''
    im_name = info['file_name']
    im_path = os.path.join(im_dir,im_name)
    image = Image.open(im_path)
    iw, ih = image.size
    h, w = input_shape
    box = []
    for b in info['bboxes']:
        class_id = b['class_id']
        x,y,bw,bh = b['bbox']
#         x = int(x)
#         y = int(y)
#         w = int(w)
#         h = int(h)
        bbox = [x,y,x+bw,y+bh,class_id]
        box.append(bbox)
    box = np.array(box)
    
    # resize image
    new_ar = w/h * rand(1-jitter,1+jitter)/rand(1-jitter,1+jitter)
    scale = rand(.25, 2)
    if new_ar < 1:
        nh = int(scale*h)
        nw = int(nh*new_ar)
    else:
        nw = int(scale*w)
        nh = int(nw/new_ar)
    image = image.resize((nw,nh), Image.BICUBIC)

    # place image
    dx = int(rand(0, w-nw))
    dy = int(rand(0, h-nh))
    new_image = Image.new('RGB', (w,h), (128,128,128))
    new_image.paste(image, (dx, dy))
    image = new_image

    # flip image or not
    flip = rand()<.5
    if flip: image = image.transpose(Image.FLIP_LEFT_RIGHT)

    # distort image
    hue = rand(-hue, hue)
    sat = rand(1, sat) if rand()<.5 else 1/rand(1, sat)
    val = rand(1, val) if rand()<.5 else 1/rand(1, val)
    x = rgb_to_hsv(np.array(image)/255.)
    x[..., 0] += hue
    x[..., 0][x[..., 0]>1] -= 1
    x[..., 0][x[..., 0]<0] += 1
    x[..., 1] *= sat
    x[..., 2] *= val
    x[x>1] = 1
    x[x<0] = 0
    image_data = hsv_to_rgb(x) # numpy array, 0 to 1

    # correct boxes
    box_data = np.zeros((max_boxes,5))
    if len(box)>0:
        np.random.shuffle(box)
        box[:, [0,2]] = box[:, [0,2]]*nw/iw + dx
        box[:, [1,3]] = box[:, [1,3]]*nh/ih + dy
        if flip: box[:, [0,2]] = w - box[:, [2,0]]
        box[:, 0:2][box[:, 0:2]<0] = 0
        box[:, 2][box[:, 2]>w] = w
        box[:, 3][box[:, 3]>h] = h
        box_w = box[:, 2] - box[:, 0]
        box_h = box[:, 3] - box[:, 1]
        box = box[np.logical_and(box_w>1, box_h>1)] # discard invalid box
        if len(box)>max_boxes: box = box[:max_boxes]
        box_data[:len(box)] = box
    return image_data, box_data

def mc3_get_random_data(im_dir,info, input_shape,max_boxes=5):
    '''random preprocessing for real-time data augmentation'''
    im_name = info['file_name']
    im_path = os.path.join(im_dir,im_name)
    image = Image.open(im_path)
    iw,ih = image.size[:2]
    h, w = input_shape
    box = []
    
    # resize image
    if iw/ih > w/h:
        nw = w
        nh = int(nw/iw * ih)
    else:
        nh = h
        nw = int(nh/ih * iw)
    new_image = image.resize((nw,nh), Image.BICUBIC)
    pad_image = Image.new('RGB', (w,h), (0,0,0))
    pad_image.paste(new_image, (0,0))
    pad_image = np.array(pad_image,dtype=np.float64)
    pad_image = pad_image/255

    dx = nw/iw
    dy = nh/ih
    box_data = np.zeros((max_boxes,5))
    for b in info['bboxes']:
        class_id = b['class_id']
        x,y,w,h = b['bbox']
        x = x*dx
        w = w*dx
        y = y*dy
        h = h*dy
        bbox = [x,y,x+w,y+h,class_id]
        box.append(bbox)
    box = np.array(box)
    box_data[:len(box)] = box
    
    return pad_image,box_data
