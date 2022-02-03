from collections import Counter
import pandas as pd

attribute_Data = pd.read_csv('../DeepFashion/attribute_predict/anno/list_attr_img_new_7500.csv',header=None)
attribute_dataset = attribute_Data.values

# print(attribute_Data.head(5))

attribute_x = attribute_dataset[:,0]
attribute_y = attribute_dataset[:,1:1001]   # 2차원 배열  [[-1,-1,...-1], ... ,[-1,-1,-1,...,-1]]  # attribute_y[0],...attribute_y[7600]


# print(len(attribute_y[0]))  #1000
# print(attribute_y[0][999])
# print(attribute_x[0])

attr_cloth_Data = pd.read_csv('../DeepFashion/attribute_predict/anno/list_attr_cloth_new.csv',header=None)
attr_cloth_dataset = attr_cloth_Data.values

ac_x = attr_cloth_dataset[:,0]  # 속성 이름
ac_y = attr_cloth_dataset[:,1]  # 속성 타입

att_1 = []    # attribute_type이 1인 것들의 인덱스 저장   1, 2, 3, ... ,991, 992
att_2 = []    # attribute type이 2인 것들의 인덱스 저장   14, 15, 21, ... ,970, 983
att_total_12 = []
img_list = []   # img_list는 이미지 경로와, 해당 이미지가 1값을 가지고 있는 속성의 인덱스 값들을 저장함   ex) [[img001, 31, 100, 64], [img002, 30, 10, 3], ... , ]]
#print(ac_x[0],ac_y[0])

len_count = []

for i, d in enumerate(attribute_y):
    img_list.append([])
    for a, b in enumerate(attribute_y[i]):
        if b == 1:
            img_list[i].append(a)
    len_count.append(len(img_list[i]))

len_counter = Counter(len_count)
print(len_counter)
