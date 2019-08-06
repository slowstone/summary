import socket
import sys
import os
sys.path.append('./gen-py')

import logging
logging.basicConfig()

from top_k import top_k
from top_k.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
import numpy as np
import cv2
import pickle

def aHash(img,size=(512,512)):
    img=cv2.resize(img,size,interpolation=cv2.INTER_CUBIC)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    s=0
    hash_str=''
    for i in range(size[0]):
        for j in range(size[1]):
            s=s+gray[i,j]
    avg=s/(size[0]*size[1])
    for i in range(size[0]):
        for j in range(size[1]):
            if  gray[i,j]>avg:
                hash_str=hash_str+'1'
            else:
                hash_str=hash_str+'0'            
    return hash_str

def hammingDistance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))

class topkHandler:
    def top_k(self,photo,k):
        rec_im = pickle.loads(photo)
        print("============receive==========")
        print("Receive im_string from client")
        print("The string len:",type(photo),len(photo))
        print("String deencoded into image")
        print("The image shape is : ",type(rec_im),np.shape(rec_im))
        
        data_dir = './dataset'
        rec_hash = aHash(rec_im)
        names = os.listdir(data_dir)
        res = []
        for name in names:
            im_path = os.path.join(data_dir,name)
            cur_im = cv2.imread(im_path)
            cur_hash = aHash(cur_im)
            score = hammingDistance(rec_hash,cur_hash)
            res.append((name,score))
        
        res.sort(key=lambda x:x[1])
        send_names = [ t[0] for t in res[:k]]
        
        send_string_list = []
        for i,name in enumerate(send_names):
            send_im = cv2.imread(os.path.join(data_dir,name))
            send_string = pickle.dumps(send_im)
            print("=========send image {}-{}===========".format(i+1,name))
            print("Send image to server")
            print("The image shape is:",send_im.shape)
            print("image encoded into string.")
            print("The string len:",type(send_string),len(send_string))
            send_string_list.append(send_string)
    
#         f = open('server.png','wb')
#         f.write(photo)
#         f.close()

#         f = open('./bird02.png','rb')
#         send_string = f.read()
#         f.close()
        
        return send_string_list
        
try:
    handler = topkHandler()

    processor = top_k.Processor(handler)

    transport = TSocket.TServerSocket("localhost", 9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    print("Starting thrift server in python...")
    server.serve()
    print("done!")
except Thrift.TException as ex:
    print("%s"%(ex.message))