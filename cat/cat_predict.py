#-*- coding: utf-8 -*-

import sys, os
import matplotlib.pyplot as plt
from matplotlib.image import imread
from keras.utils import np_utils
from keras.models import load_model
from PIL import Image
import numpy as np

def category_total():
  
    f = open('list_category_cloth.csv','r')

    while(True):
        lines = f.read().splitlines()
        if not lines:
            break

        categories = []; tmp_cat = []
        for i, d in enumerate(lines):
            tmp = lines[i]
            num_index = len(lines[i]) - 2 
            tmp_cat = tmp[:num_index]
            categories.append(tmp_cat)
            categories.sort()

    f.close()
    
    #image_files = ['plaid_cam.jpg']
    image_files = ['camera.png']
    image_size = 64

    X = []; files = []

    for fname in image_files:
        img = Image.open(fname)
        img = img.crop((270,6,950,720))
        img.save("img2.png")
        img = img.convert("RGB")
        img = img.resize((image_size, image_size))
        in_data = np.asarray(img)
        in_data = in_data.astype("float") / 256
        X.append(in_data)
        files.append(fname)

    X = np.array(X)

    #model = load_model('category_cropped_01.h5')
    model = load_model('category_cropped_02.h5')   # 데모에서 우리를 구해준 효자 모델
    #model = load_model('category_cropped_03.h5')
    #model = load_model('model/6layer_category_cl_01.h5')   # 데모에서 우리를 구해준 효자 모델  

    pre = model.predict(X)

    for i, p in enumerate(pre):
        y = p.argmax()
       # print("입력:", files[i])    # 정답
       # print("예측:", "[", y, "]",categories[y], "/ Score",p[y])

    text = categories[y]
    #print(text)
    score = int(p[y] * 1000) / 10
    score_txt = str(score) + '%'
    #text = categories[y]
    return text,score_txt 

category_total()

