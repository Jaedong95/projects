from sklearn.model_selection import train_test_split
from PIL import Image
import os, glob
import numpy as np


import os
import pandas as pd
import numpy as np
import shutil
import pandas as pd



img_Data = pd.read_csv('../DeepFashion/attribute_predict/anno/list_category_img.csv',header=None)

img_dataset = img_Data.values

#total_x = img_dataset[:,0]
#total_y = img_dataset[:,1]

'''그래프 출력용'''
total_x = img_dataset[0:30000,0]
total_y = img_dataset[0:30000,1]

f = open('../DeepFashion/attribute_predict/anno/list_category_cloth.csv','r')

path = '../DeepFashion/attribute_predict/category/'

types = [];
cat = [];
tmp_cat = [];
cat_name = []

while(True):
    lines = f.read().splitlines()   # ['Anorak,1', 'Blazer,1', 'Blouse,1', ... , 'Sundress,3']

    if not lines:
        break

    for i, d in enumerate(lines):
        tmp = lines[i]      # 'Anorak,1'
        num_index = len(lines[i]) - 2
        tmp_cat = tmp[:num_index]   # 'Anorak'
        cat.append(tmp_cat)


print(cat)

root_dir = '../DeepFashion/attribute_predict/category/'


img_len = 64

X = []
Y = []

for idx, category in enumerate(cat):
    image_dir = root_dir + category
    files = glob.glob(image_dir + "/" + "*.jpg")

    for i, f in enumerate(files):  # enumerate 수행 시 idx, data 반환   13만장, 5만장, 9만장
        # 이미지 로딩 (3)
        img = Image.open(f)
        img = img.convert("RGB")
        img = img.resize((img_len, img_len))
        data = np.asarray(img)
        X.append(data)
        Y.append(idx)

X = np.array(X)
Y = np.array(Y)

#print(X)

# 학습 데이터와 테스트 데이터 나누기 (4)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y)

xy = (X_train, X_test, Y_train, Y_test)

#np.save(root_dir + "clothes_category_increase.npy",xy)
np.save(root_dir + "cat_graph.npy",xy)
