import os
import pandas as pd
import numpy as np
import shutil
import pandas as pd


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


img_Data = pd.read_csv('../DeepFashion/attribute_predict/anno/list_category_img.csv',header=None)

img_dataset = img_Data.values

#total_x = img_dataset[:,0]
#total_y = img_dataset[:,1]

'''그래프 출력용'''
total_x = img_dataset[0:30000,0]
total_y = img_dataset[0:30000,1]

''' 파일 이름 변환 '''
split_name = []
tmp = [[0]*3 for i in range(len(total_x))]  # [[0,0,0], [0,0,0], ... ,[0,0,0]]

translate_name = []
table = str.maketrans('/','_')

for i, d in enumerate(total_x):
    tmp[i] = total_x[i].split('/')
    new_image = tmp[i][1] + '/' + tmp[i][2]    # img, Paisley_Fit_&_Flare_Dress, img0000000001.jpg -> img 제거
    split_name.append(new_image)
    translate_name.append(d.translate(table))   #  Paisley_Fit_&_Flare_Dress_img00000001.jpg 형태

# print(translate_name)
''' 폴더 만들기 '''
f = open('../DeepFashion/attribute_predict/anno/list_category_cloth.csv','r')
path = '../DeepFashion/attribute_predict/category/'

img_path = '../DeepFashion/attribute_predict/'
dest_dir = '../DeepFashion/attribute_predict/category/'  # sample 을 위한 폴더 생성 ( up_down = 전체 28만장 )

while(True):
    lines = f.read().splitlines()   # ['Anorak,1', 'Blazer,1', 'Blouse,1', ... , 'Sundress,3']
    types = []; cat = []; dest = []; tmp_cat = []; cat_name = []

    if not lines:
        break
    #print(lines)
    for i, d in enumerate(lines):
        tmp = lines[i]      # 'Anorak,1'
        num_index = len(lines[i]) - 2
        tmp_cat = tmp[:num_index]   # 'Anorak'
        dest = path + tmp_cat
        cat.append([])
        cat_name.append([])
        cat[i].append(tmp_cat)
        cat_name[i].append(tmp_cat)
        #print(cat[i])
        createFolder(dest)
    #print(cat)
    #print(cat[2][0])

    # total_y = category 값, 1~50

    for i, d in enumerate(total_y):  # 28만번 수행  , d = 1~50
        #print(i, d)
        index = d - 1
        cat[index].append(total_x[i])
        cat_name[index].append(translate_name[i])
    #print(cat_name)
    #print(cat[49][0])
    #print(len(cat[41]))
    #print(cat_name)
    #print(i)

    for i, category in enumerate(cat):
        #print(cat[i][0])   #  Anorak, Caftan, ...
        #print(len(cat[i]))
        #print(cat[i])
        #print(cat_name[i])
        #print(i)
        for a, b in zip(cat[i],cat_name[i]):   # b = cat[0]
            #print(a, b)   a = img/kimono-sleeved_paisley_Blouse/img_00001.jpg    b = img_Kimono-Sleeved_Paisely_Blouse_img_00001.jpg
            if '.jpg' in a:
                clothes_dir = img_path + a
                result_file_path_name = dest_dir + cat[i][0] + '/' + b
                #print(clothes_dir)
                #print(result_file_path_name)
                shutil.copy(clothes_dir, result_file_path_name)

f.close