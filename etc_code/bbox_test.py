import pandas as pd
from PIL import Image

bbox_Data = pd.read_csv('../DeepFashion/attribute_predict/anno/list_bbox.csv', header=None)
bbox_dataset = bbox_Data.values

img_name = bbox_dataset[1:10,0]
img_bbox = bbox_dataset[1:10,1:5]

path = '../DeepFashion/attribute_predict/'
dest_dir = '../../Desktop/'

split_name = []
tmp = [[0]*3 for i in range(len(img_name))]
translate_name = []
table = str.maketrans('/','_')

for i, d in enumerate(img_name):
    tmp[i] = img_name[i].split('/')
    new_image = tmp[i][1] + '/' + tmp[i][2]
    split_name.append(new_image)
    translate_name.append(d.translate(table))

print(translate_name)

for i, d in enumerate(img_name):
    clothes_dir = path + d
    print(img_bbox[i])
    img = Image.open(clothes_dir)
    img2 = img.crop((img_bbox[i][0], img_bbox[i][1], img_bbox[i][2], img_bbox[i][3]))
    img2.save('../../Desktop/' + translate_name[i])
