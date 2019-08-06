import json
from urllib import request
import os

image_dir = './image_men/'
image_name_list = os.listdir(image_dir)
f = open('./output_men_new.json','r')
info = json.load(f)
sum_num = len(info)
wf = open('./log_men.txt','w')

for num,i in enumerate(info):
    url = i['im_url']
    try:
        name_list = url.split('/')
        name = name_list[-2] + "-" + name_list[-1]
        if name in image_name_list:
            continue
        path = os.path.join(image_dir,name)
        request.urlretrieve(url, path)
        print('Done' , num , '/' , sum_num, end='\r')
    except Exception as e:
        wf.write(url+' '+str(e)+'\n')
        pass