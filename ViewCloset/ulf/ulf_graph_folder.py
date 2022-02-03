import os
import pandas as pd
import numpy as np
import shutil
import string

img_Data = pd.read_csv('../DeepFashion/attribute_predict/anno/list_category_img.csv',header=None)
img_dataset = img_Data.values

# 상의: 139709장  하의: 58963장  한벌옷: 90550 장

img_x = img_dataset[0:10000, 0]
img_y = img_dataset[0:10000, 1]

img_x1 = img_dataset[140000:150000, 0]
img_y1 = img_dataset[140000:150000, 1]

img_x2 = img_dataset[230000:240000, 0]
img_y2 = img_dataset[230000:240000, 1]

tmp_x = np.concatenate((img_x, img_x1))
tmp_y = np.concatenate((img_y, img_y1))

total_x = np.concatenate((tmp_x, img_x2))
total_y = np.concatenate((tmp_y, img_y2))

split_name = []
tmp = [[0]*3 for i in range(len(total_x))]
translate_name = []
table = str.maketrans('/','_')

for i, d in enumerate(total_x):
    tmp[i] = total_x[i].split('/')
    new_image = tmp[i][1] + '/' + tmp[i][2]
    split_name.append(new_image)
    translate_name.append(d.translate(table))

Up = []
Up_name = []
Low = []
Low_name = []
Full = []
Full_name = []

#split_name = 'Front_Blouse/0000001.jpg'
#translate_name = 'Front_Blouse_000001.jpg'

# category가 1~20일 경우 category type = 1, category가 21~36일 경우 category type = 2  category가 37~50일 경우 category = 3
for i,img in enumerate(total_y):
    if img >= 1 and img <=20: #  print("상의:%d",img) .. ok
        Up.append(split_name[i])
        Up_name.append(translate_name[i])
    elif img >= 21 and img <= 36:  #  print("하의:%d",img) .. ok
        Low.append(split_name[i])
        Low_name.append(translate_name[i])
    elif img >= 37 and img <= 50:  #  print("한벌옷:%d",img) .. ok
        Full.append(split_name[i])
        Full_name.append(translate_name[i])

# upper_clothes[0] => img/sheer_front_blouse/img00000001.jpg 형식
# 이미지 파일을 하나로 합칠 때 중복되는 이미지명을 피라기 위해서 '/' 를 '_'로 바꿔줌
# table = str.maketrans('/','_')

path = '../DeepFashion/attribute_predict/img/'
root_dir = '../DeepFashion/attribute_predict/up_down/'  # sample 을 위한 폴더 생성 ( up_down = 전체 28만장 )

for i,filename in enumerate(Up):
    up_clothes_dir = path + filename
    result_file_path_name = root_dir + 'Up/' + Up_name[i]
    shutil.copy(up_clothes_dir, result_file_path_name)

for i, filename in enumerate(Low):
    down_clothes_dir = path + filename
    result_file_path_name = root_dir + 'Low/' + Low_name[i]
    shutil.copy(down_clothes_dir, result_file_path_name)

for i, filename in enumerate(Full):
    full_clothes_dir = path + filename
    result_file_path_name = root_dir + 'Full/' + Full_name[i]
    shutil.copy(full_clothes_dir, result_file_path_name)
