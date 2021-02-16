from IPython.core.display import HTML
from IPython.display import Image
from collections import Counter
import pandas as pd
import json


from plotly.offline import init_notebook_mode, iplot
import matplotlib.pyplot as plt
import plotly.graph_objs as go
#from wordcloud import WordCloud
from plotly import tools
import seaborn as sns
from PIL import Image

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
#print(img_list)
dump = []
#print(ac_x[0],ac_y[0])

for i, d in enumerate(attribute_y):
    img_list.append([])
    for a, b in enumerate(attribute_y[i]):
        if b == 1:
            img_list[i].append(a)

# print(img_list)  # 이미지가 어떤 라벨에 해당하는지 모두 출력

for i, d in enumerate(img_list):
    for a, b in enumerate(img_list[i]):
        #print(b)
        if ac_y[b] == 1:
            att_1.append(b)
            att_total_12.append(b)
        elif ac_y[b] == 2:
            att_2.append(b)
            att_total_12.append(b)
        else:
            dump.append(b)

#print(att_1)
#print(len(dump))
#print(len(img_list))
#print(len(att_1))
#print(len(att_2))
#print(len(att_total_12))

counter = Counter(att_total_12)

print(counter)

xValues = list(counter.keys())
yValues = list(counter.values())

# print(xValues)
# print(yValues)

trace1 = go.Bar(x=xValues, y=yValues, opacity=0.8, name="year count", marker=dict(color='rgba(20, 20, 20, 1)'))
layout = dict(width=800, title='Distribution of different labels in the train dataset', legend=dict(orientation="h"));

fig = go.Figure(data=[trace1], layout=layout);
iplot(fig);