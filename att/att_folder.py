import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.image import imread

attribute_Data = pd.read_csv('../../DeepFashion/attribute_predict/anno/list_attr_img_new_7500.csv',header=None)
attribute_dataset = attribute_Data.values

# print(attribute_Data.head(5))

attribute_x = attribute_dataset[:,0]
attribute_y = attribute_dataset[:,1:1001]   # 2차원 배열  [[-1,-1,...-1], ... ,[-1,-1,-1,...,-1]]  # attribute_y[0],...attribute_y[7600]

# print(len(attribute_y[0]))  1000
# print(attribute_y[0][999])
# print(attribute_x[0])

attr_cloth_Data = pd.read_csv('../../DeepFashion/attribute_predict/anno/list_attr_cloth_new.csv',header=None)
attr_cloth_dataset = attr_cloth_Data.values

ac_x = attr_cloth_dataset[:,0]
ac_y = attr_cloth_dataset[:,1]

att_1 = []    # attribute_type이 1인 것들의 인덱스 저장   1, 2, 3, ... ,991, 992
att_2 = []    # attribute type이 2인 것들의 인덱스 저장   14, 15, 21, ... ,970, 983
img_list = []   # img_list는 이미지 경로와, 해당 이미지가 1값을 가지고 있는 속성의 인덱스 값들을 저장함   ex) [[img001, 31, 100, 64], [img002, 30, 10, 3], ... , ]]
#print(img_list)

#print(ac_x[0],ac_y[0])

for i, d in enumerate(attribute_y):
    #print(i)   1,2,...,7603
    #print(d)   -1,-1,...,-1 7603번 반복
    img_list.append([])
    #print(img_list[i])    제대로 [[][]...[][]] 만들어졌다.
    img_list[i].append(attribute_x[i])
    #print(img_list[i])     제대로 들어왔다.

    for a, b in enumerate(attribute_y[i]):
        # print(a)  0,1,2,...999 까지  7603번 반복
        # print(b) -1,-1,...,-1 7603번 반복
        if b == 1:
            img_list[i].append(a)

# print(img_list)  # [[img01, 10, 12, 32], [img02, 100, 391], ... , [img7604, 114, 705, 720, 822]]
# print(len(img_list)) 7604 길이의 이차원 배열

'''  어떤 속성이 얼마나 들어 있는지 계산 
#for i, d in enumerate(img_list):
    #print(d)
    #for a,b in enumerate(img_list[i]):
'''

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


path = '../../DeepFashion/attribute_predict/attribute/'

for i, d in enumerate(ac_y):
    if(d == 1):
        #print(i) # 0 = 3 이기 때문에 1(abstract)부터 시작 ~
        att_1.append(i)
        #print(ac_x[i], i)
        dest = path + ac_x[i]
        createFolder(dest)
    elif(d == 2):
        #print(i)
        att_2.append((i))
        dest = path + ac_x[i]
        createFolder(dest)

# print(len(att_1))
# print(len(att_2))

''' 폴더에 들어갈 이미지의 이름 변경 '''
split_name = []
tmp = [[0]*3 for i in range(len(attribute_x))]  # [[0,0,0], [0,0,0], ... ,[0,0,0]]

translate_name = []
table = str.maketrans('/','_')

img_path = '../../DeepFashion/attribute_predict/'
dest  = '../../DeepFashion/attribute_predict/attribute/'

for i, d in enumerate(attribute_x):     #attribute_x = img_name
    tmp[i] = attribute_x[i].split('/')
    new_image = tmp[i][1] + '/' + tmp[i][2]    # img, Paisley_Fit_&_Flare_Dress, img0000000001.jpg -> img 제거
    split_name.append(new_image)
    translate_name.append(d.translate(table))   # Paisley_Fit_&_Flare_Dress_img00000001.jpg 형태
    #print(d.translate(table))


for i, d in enumerate(img_list):
    # print(img_list[i][0])
    for a, b in enumerate(img_list[i]):
        if b in att_1:   # 34가 att_1 배열에 있다면 -> 34번째 속성에 해당하는 폴더를 찾아서 해당 폴더에 img_list[i][0]을 집어넣어줌
            # print(ac_x[b])   폴더 명 (abstract, floral, watercolor)
            underbar_img = img_list[i][0].translate(table)
            #print(underbar_img, img_list[i][0])   # 변환 완료, 원본 유지 완료
            dest_dir = dest + ac_x[b] + '/' + underbar_img
            clothes_dir = img_path + img_list[i][0]
          #  print(dest_dir)
            shutil.copy(clothes_dir, dest_dir)
        elif b in att_2:
            underbar_img = img_list[i][0].translate(table)
            # print(underbar_img, img_list[i][0])    변환 완료, 원본 유지 완료
            dest_dir = dest + ac_x[b] + '/' + underbar_img
            clothes_dir = img_path + img_list[i][0]
            shutil.copy(clothes_dir, dest_dir)