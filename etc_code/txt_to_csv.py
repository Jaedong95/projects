import tensorflow as tf
import os
import pandas as pd
import numpy as np
import shutil
import string

f = open('../DeepFashion/attribute_predict/anno/list_attr_cloth.txt','r')
new = open('../DeepFashion/attribute_predict/anno/list_attr_cloth_new.txt','w')

while True:
    lines = f.readlines()
    if not lines:
        break
    tmp = []; s1 = []; s2 = ' ';  s3 = []; final_lines = []

    for i, d in enumerate(lines):
        tmp = lines[i].replace(' ','')
        num_index = len(tmp) - 2
        # 문자열 저장. no_blank[i][:num_index] 보다 tmp[:num_index]로 해야 될 거 같음
        s1 = tmp[:num_index]
        s3 = tmp[num_index: ]    # 이로써 단어와 숫자가 분리됨
        new.write(s1+s2+s3)
        #print(final_lines)

        # 이제 이걸로 txt 파일 만들고, csv 파일로 변환하면 끝!
    #print(final_lines)

f.close()
new.close()