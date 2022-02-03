from sklearn.model_selection import train_test_split
from PIL import Image
import os
import glob
import pandas as pd
import numpy as np

root_dir = '../../DeepFashion/attribute_predict/attribute/'

# f = open('../../Classify_ulf/list_category_cloth.csv','r')
attr_cloth_Data = pd.read_csv('../../DeepFashion/attribute_predict/anno/list_attr_cloth_new.csv',header=None)
# attr_cloth_dataset = attr_cloth_Data.values

idx = attr_cloth_Data[attr_cloth_Data[1] == 3].index
attr_cloth_Data_1 = attr_cloth_Data.drop(idx)
idx2 = attr_cloth_Data_1[attr_cloth_Data_1[1] == 4].index
attr_cloth_Data_2 = attr_cloth_Data_1.drop(idx2)
idx3 = attr_cloth_Data_2[attr_cloth_Data_2[1] == 5].index
attr_cloth_Data_3 = attr_cloth_Data_2.drop(idx3)
attr_cloth_dataset = attr_cloth_Data_3.values

att_name = attr_cloth_dataset[:,0]
att_type = attr_cloth_dataset[:,1]

print(att_name)
print(len(att_name))

nb_classes = len(att_name)

img_len = 64

X = []
Y = []

for idx, attribute in enumerate(att_name):
    image_dir = root_dir + attribute
    files = glob.glob(image_dir + "/" + "*.jpg")
    # print(image_dir + "/" + "*.jpg")
    # print(files)
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

X_train, X_test, Y_train, Y_test = train_test_split(X, Y)

xy = (X_train, X_test, Y_train, Y_test)

#np.save(root_dir + "clothes_attribute.npy",xy)

'''그래프 출력용'''
np.save(root_dir + "att_graph.npy",xy)