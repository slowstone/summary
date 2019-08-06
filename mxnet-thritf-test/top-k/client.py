import sys
sys.path.append('./gen-py')
from top_k import top_k

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import pickle
import cv2
import numpy as np

try:
    transport = TSocket.TSocket('localhost', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = top_k.Client(protocol)
    transport.open()

    send_im = cv2.imread('./test2.jpg')
    send_string = pickle.dumps(send_im)
    print("Send image to server")
    print("The image shape is:",send_im.shape)
    print("image encoded into string.")
    print("The string len:",type(send_string),len(send_string))
    rec_string_list = client.top_k(send_string,3)
    for i,rec_string in enumerate(rec_string_list):
        rec_im = pickle.loads(rec_string)
        print("========receive  image  {}==========".format(i+1))
        print("Receive im_string from client")
        print("The string len:",type(rec_string),len(rec_string))
        print("String deencoded into image")
        print("The image shape is : ",type(rec_im),np.shape(rec_im))
        rec_path = './client/image_{}.png'.format(i+1)
        cv2.imwrite(rec_path,rec_im)
        

#     f = open('./bird01.png','rb')
#     send_data = f.read()
#     f.close()
#     rec_data = client.top_k(send_data,1)

#     f = open('client.png','wb')
#     f.write(rec_data)
#     f.close()
    
    transport.close()

except Thrift.TException as ex:
    print("%s"%(ex.message))