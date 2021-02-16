import os
import pandas as pd
import numpy as np
import shutil
import string

img_Data = pd.read_csv('../DeepFashion/attribute_predict/anno/list_category_img.csv',header=None)

'''
print(img_Data.head())
print(img_Data.shape)
'''

img_dataset = img_Data.values

# 상의: 139709장  하의: 58963장  한벌옷: 90550 장

img_x = img_dataset[0:100, 0]
img_y = img_dataset[0:100, 1]

img_x1 = img_dataset[140000:140100, 0]
img_y1 = img_dataset[140000:140100, 1]

img_x2 = img_dataset[230000:230100, 0]
img_y2 = img_dataset[230000:230100, 1]

tmp_x = np.concatenate((img_x, img_x1))
tmp_y = np.concatenate((img_y, img_y1))

total_x = np.concatenate((tmp_x, img_x2))
total_y = np.concatenate((tmp_y, img_y2))

split_name = []
tmp = [[0]*3 for i in range(len(total_x))]
translate_name = []
table = str.maketrans('/','_')

#print(tmp)

for i, d in enumerate(total_x):
    tmp[i] = total_x[i].split('/')
    new_image = tmp[i][1] + '/' + tmp[i][2]
    split_name.append(new_image)
    translate_name.append(d.translate(table))

# for i, d in enumerate(split_name):

# print(split_name)   # 새로운 이미지 이름 지정 완료.
# print(translate_name)

upper_clothes = []
lower_clothes = []
full_clothes = []

# category가 1~20일 경우 category type = 1, category가 21~36일 경우 category type = 2  category가 37~50일 경우 category = 3
for i,img in enumerate(total_y):
    if img >= 1 and img <=20: #  print("상의:%d",img) .. ok
        upper_clothes.append(split_name[i])
    elif img >= 21 and img <= 36:  #  print("하의:%d",img) .. ok
        lower_clothes.append(split_name[i])
    elif img >= 37 and img <= 50:  #  print("한벌옷:%d",img) .. ok
        full_clothes.append(split_name[i])

# print(upper_clothes[10])
# print(lower_clothes[0])
# print(full_clothes[0])

'''
print(len(upper_clothes))
print(len(lower_clothes))
print(len(full_clothes))
print(upper_clothes[0:10])
print(lower_clothes[0:10])
print(full_clothes[0:10])
'''

path = '../DeepFashion/attribute_predict/img/'
root_dir = '../DeepFashion/attribute_predict/test/'  # sample 을 위한 폴더 생성 ( up_down = 전체 28만장 )

for i,filename in enumerate(upper_clothes):
    up_clothes_dir = path + filename
    result_file_path_name = root_dir + 'up/' + translate_name[i]
    shutil.copy(up_clothes_dir, result_file_path_name)

for i, filename in enumerate(lower_clothes):
    down_clothes_dir = path + filename
    result_file_path_name = root_dir + 'down/' + translate_name[i]
    shutil.copy(down_clothes_dir, result_file_path_name)

for i, filename in enumerate(full_clothes):
    full_clothes_dir = path + filename
    result_file_path_name = root_dir + 'full/' + translate_name[i]
    shutil.copy(full_clothes_dir, result_file_path_name)
