import pandas as pd
from PIL import Image

bbox_Data = pd.read_csv('../DeepFashion/attribute_predict/anno/list_bbox.csv', header=None)
bbox_dataset = bbox_Data.values

img_name = bbox_dataset[:,0]
img_bbox = bbox_dataset[:,1:5]

path = '../DeepFashion/attribute_predict/'

for i, d in enumerate(img_name):
    clothes_dir = path + d
    #print(img_bbox[i])
    img = Image.open(clothes_dir)
    img2 = img.crop((img_bbox[i][0], img_bbox[i][1], img_bbox[i][2], img_bbox[i][3]))
    img2.save(clothes_dir)

