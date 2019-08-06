import mxnet as mx
import os
import numpy as np
def get_iterators(train_path,val_path,batch_size, data_shape=(3, 224, 224)):
    train = mx.io.ImageRecordIter(
        path_imgrec         = train_path,
        data_name           = 'data',
        label_name          = 'softmax_label',
        batch_size          = batch_size,
        data_shape          = data_shape,
        resize              = 224,
        shuffle             = True,
        rand_crop           = False,
        rand_mirror         = True)
    val = mx.io.ImageRecordIter(
        path_imgrec         = val_path,
        data_name           = 'data',
        label_name          = 'softmax_label',
        batch_size          = batch_size,
        data_shape          = data_shape,
        resize              = 224,
        rand_crop           = False,
        rand_mirror         = False)
    return (train, val)

def get_fine_tune_model(symbol, arg_params, num_classes, layer_name='flatten0'):
    """
    symbol: the pretrained network symbol
    arg_params: the argument parameters of the pretrained model
    num_classes: the number of classes for the fine-tune datasets
    layer_name: the layer name before the last fully-connected layer
    """
    all_layers = symbol.get_internals()
    net = all_layers[layer_name+'_output']
    net = mx.symbol.FullyConnected(data=net, num_hidden=num_classes, name='fc1')
    net = mx.symbol.SoftmaxOutput(data=net, name='softmax')
    new_args = dict({k:arg_params[k] for k in arg_params if 'fc1' not in k})
    return (net, new_args)

def train(symbol, arg_params, aux_params, train, val, batch_size, num_epoch, params,
          gpus = 0, CHECKPOINT_PATH = None):
    if len(gpus) == 0:
        devs = mx.cpu()
    else:
        devs = [mx.gpu(i) for i in gpus]
    
    
    if not CHECKPOINT_PATH is None:
        epoch_end_callbacks = [
            mx.callback.do_checkpoint(CHECKPOINT_PATH, 1)
        ]
    else:
        epoch_end_callbacks = []
        
    batch_end_callbacks = [
        mx.callback.Speedometer(batch_size, 10)
    ]
    mod = mx.mod.Module(symbol=symbol, context=devs)
    mod.fit(train, val,
        num_epoch=num_epoch,
        arg_params=arg_params,
        aux_params=aux_params,
        allow_missing=True,
        batch_end_callback = batch_end_callbacks,
        epoch_end_callback = epoch_end_callbacks,
        kvstore='device',
        optimizer='sgd',
        optimizer_params=params,
        initializer=mx.init.Xavier(rnd_type='gaussian', factor_type="in", magnitude=2),
        eval_metric='acc')
    metric = mx.metric.Accuracy()
    return mod.score(val, metric)

if __name__ == '__main__':
    import argparse
    import logging
    head = '%(asctime)-15s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=head)
    
    parser = argparse.ArgumentParser(description='Network Params')
    parser.add_argument('-pretrain_model', type=str,
                        help='path to pretrain_model. eg: /path/to/resnet-50',
                        default='/mnt/cephfs/lab/xuyan.bupt/model/resnet/resnet-50')
    parser.add_argument('-pretrain_epoch', type=int,
                        help='pretrain_model epoch',
                        default=0)
    parser.add_argument('-dataset_dir', type=str,
                        help='path to cifar dataset',
                        default='/mnt/cephfs/lab/xuyan.bupt/dataset/cifar')
    parser.add_argument('-class_num', type=int,
                        help='class number of the cifar dataset',
                        default=10)
    parser.add_argument('-model_save_dir',type=str,
                        help='path to save model.',
                        default='./logs')
    parser.add_argument('-gpus',type=str,
                        help='gpu ids.such as 1,2,3.(will split by ,)',
                        default='2,3')
    parser.add_argument('-num_epoch',type=int,
                        help='the number of epoch',
                        default=20)
    parser.add_argument('-batch_size_per_dev',type=int,
                        help='batch size per gpu when using gpu. batch size when using cpu',
                        default=50)
    parser.add_argument('-lr',type=float,
                        help='learning rate',
                        default=0.001)
    args = parser.parse_args()
    
    PRETRAIN_MODEL = args.pretrain_model
    FINETUNE_MODEL = PRETRAIN_MODEL.split('/')[-1]
    FINETUNE_EPOCH = args.pretrain_epoch
    
    num_classes = args.class_num
    num_epoch = args.num_epoch
    optimizer_params = {'learning_rate':args.lr,'momentum':0.9}
    
    if not args.gpus is None:
        batch_per_gpu = args.batch_size_per_dev
        GPUS = [int(i) for i in args.gpus.split(',')]
        num_gpus = len(GPUS)
        batch_size = batch_per_gpu * num_gpus
    else:
        GPUS = []
        batch_size = args.batch_size_per_dev
    
    if args.model_save_dir != 'None':
        CHECKPOINT_DIR = args.model_save_dir
        if not os.path.exists(CHECKPOINT_DIR):
            os.makedirs(CHECKPOINT_DIR)
        import datetime
        now = datetime.datetime.now()
        CHECKPOINT_DIR = os.path.join(CHECKPOINT_DIR,"{}_{}_{:%Y%m%dT%H%M}".format(FINETUNE_MODEL,num_classes,now))
        if not os.path.exists(CHECKPOINT_DIR):
            os.makedirs(CHECKPOINT_DIR)
        CHECKPOINT_PATH = os.path.join(
            CHECKPOINT_DIR,"cifar")
    else:
        CHECKPOINT_PATH = None
    
    dataset_dir = args.dataset_dir
    train_path = os.path.join(dataset_dir,'cifar-{}-train.rec'.format(num_classes))
    val_path = os.path.join(dataset_dir,'cifar-{}-val.rec'.format(num_classes))
    
    logging.info("gpus:                 {}".format(GPUS))
    logging.info("dataset_dir:          {}".format(dataset_dir))
    logging.info("train_path:           {}".format(train_path))
    logging.info("val_path:             {}".format(val_path))
    logging.info("checkpoint_dir:       {}".format(CHECKPOINT_DIR))
    logging.info("pretrain_model:       {}".format(PRETRAIN_MODEL))
    logging.info("pretrain_epoch:       {}".format(FINETUNE_EPOCH))
    logging.info("batch_size:           {}".format(batch_size))
    logging.info("num_classes:          {}".format(num_classes))
    logging.info("num_epoch:            {}".format(num_epoch))
    logging.info("optimizer_params:     {}".format(optimizer_params))
    
    (train_iter, val_iter) = get_iterators(train_path,val_path,batch_size)
    
    sym, arg_params, aux_params = mx.model.load_checkpoint(
        PRETRAIN_MODEL, FINETUNE_EPOCH)
    (new_sym, new_args) = get_fine_tune_model(sym, arg_params, num_classes)
    
    mod_score = train(new_sym, new_args, aux_params, train_iter, val_iter, batch_size, num_epoch, optimizer_params, GPUS, CHECKPOINT_PATH)
    file_name = os.path.join(CHECKPOINT_DIR,'score.json')
    logging.info("save val score to {}".format(file_name))
    import json
    f = open(file_name,'w')
    f.write(json.dumps(mod_score,indent=2))
    f.close()