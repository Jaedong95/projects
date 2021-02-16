#-*- coding: utf-8 -*-

import sys, os
import matplotlib.pyplot as plt
from matplotlib.image import imread
import pandas as pd
from keras.utils import np_utils
from keras.models import load_model
from PIL import Image
import numpy as np

def attribute_total():
  
    attr_cloth_Data = pd.read_csv('./list_attr_cloth_new.csv',header=None)
    attr_cloth_dataset = attr_cloth_Data.values

    ac_x = attr_cloth_dataset[:,0]
    ac_y = attr_cloth_dataset[:,1]
    
    att_total = [] 
    for i, d in enumerate(ac_y):
        if d == 1:
            att_total.append(ac_x[i])
        elif d == 2:
            att_total.append(ac_x[i])
        elif d == 4:
            att_total.append(ac_x[i])
    att_total.sort()
    #print(att_total)

    
    image_files = ['./camera.png']
    #image_files = ['floral_cam.png']

    image_size = 64

    X = []; files = []

    for fname in image_files:
        img = Image.open(fname)
        img = img.crop((270, 6, 950, 720))
        img.save('camera3.png')
        img = img.convert("RGB")
        img = img.resize((image_size, image_size))
        in_data = np.asarray(img)
        in_data = in_data.astype("float") / 256
        X.append(in_data)
        files.append(fname)

    X = np.array(X)
    
    #model = load_model('model/6layer_attribute_added_01.h5')
    #model = load_model('att_cropped_01.h5')
    #model = load_model('att_cropped_02.h5')
    #model = load_model('att_cropped_03.h5')
    # att_cropp_02.h5 -> 데모에서 우리를 구해준 효자 모델
    model = load_model('att_cropp_02.h5')
    #model = load_model('att_124_cropp_02.h5')
    #model = load_model('att_cropp_03.h5')

    pre = model.predict(X)
    #print(pre)

    for i, p in enumerate(pre):
        y = p.argmax()
        #print("입력:", files[i])    
        #print("예측:", "[", y, "]",att_total[y], "/ Score",p[y])

    text = att_total[y]
    #print(text)
    score = int(p[y] * 1000) / 10
    score_txt = str(score) + '%'
    #print(score_txt)
    return text,score_txt


attribute_total()

