import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.image import imread

attribute_Data = pd.read_csv('../DeepFashion/attribute_predict/anno/list_attr_img_new.csv',header=None)
attribute_dataset = attribute_Data.values

#print(attribute_Data.head(5))

attribute_x = attribute_dataset[:,0]
attribute_y = attribute_dataset[:,1:1001]

# print(attribute_y[0][999])
# print(attribute_x[0])

attr_cloth_Data = pd.read_csv('../DeepFashion/attribute_predict/anno/list_attr_cloth_new.csv',header=None)
attr_cloth_dataset = attr_cloth_Data.values

ac_x = attr_cloth_dataset[:,0]
ac_y = attr_cloth_dataset[:,1]

#print(ac_x[0],ac_y[0])

attribute_name = input("attribute_name을 입력해주세요")
attribute_name = attribute_name.lstrip()   # 왼쪽 공백을 제거
att_idx = 0

# 어트리뷰트 이름을 입력받으면 해당 애트리뷰트가 어디있는지 인덱스 값을 찾아서 돌려줌
for i, d in enumerate(ac_x):
    #print(i)
    if attribute_name == d:
        print("일치하는 attribute를 찾았습니다.")
        att_idx = i
        break
    '''  
    else:
        # print("일치하는 attribute가 없습니다.")
        #print(i)
    '''

idx = 0
img_list = []

#print(attribute_y[0])
#print(attribute_x[0])

''' 첫번째 이미지가 어떤 애트리뷰트에 해당하는지 출력해봄  -> 717 pleated, 818 sheer    
for i,f in enumerate(attribute_y[20]):
    # print(i, f)
    if f ==  1:
        #print(i, f)
        print(i, ac_x[i])
'''
# print(attribute_y[10][att_idx])

for i,n in enumerate(attribute_x):
    if attribute_y[i][att_idx] == 1:
        # print(attribute_x[i])
        img_list.append(attribute_x[i])

# print(img_list)    제대로 들어온다. 차례로 출력만 해주면 ok.

path = '../DeepFashion/attribute_predict/'

plt.figure(figsize=(10,10))

for i,m in enumerate(img_list):
    # print(i)
    img = imread(path + m)
    '''
    plt.subplot(10,10,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    '''
    plt.imshow(img)
    plt.xlabel(img_list[i])
    plt.show()
