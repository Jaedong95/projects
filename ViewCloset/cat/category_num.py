import pandas as pd
import numpy as np

f = open('../DeepFashion/attribute_predict/anno/list_category_img.csv','r')

num_array = []

for i in range(0,50):
    i = i +1
    num_array.append(i)

#print(num_array)

while(True):
    lines = f.read().splitlines()
    types = []
    tmp1 = []
    category_num = []
    if not lines:
        break
    #print(lines)

    for i, d in enumerate(lines):
        tmp = lines[i]
        num_index = len(lines[i]) - 2
        #print(tmp[num_index])
        if(tmp[num_index] == ','):
            num_index = len(lines[i]) - 1
        tmp1 = tmp[num_index:]
        #print(tmp1)
        category_num.append(tmp1)

    #print(category_num)
    df = pd.DataFrame({'label': category_num})
    #print(len(df['label']))
    #print(df['label'])
    #print(df.groupby('label').count())

    print(df["label"].groupby(df["label"]).count())

    # print(len(category_num))    289,222개
    '''for i in num_array:
        category_num.group'''

f.close
