
from sklearn.model_selection import train_test_split
from PIL import Image
import os, glob
import numpy as np

root_dir = '../DeepFashion/attribute_predict/ud/'

categories = ["Full","Low","Up"]
nb_classes = len(categories)

img_len = 64

X = []
Y = []

for idx, category in enumerate(categories):
    image_dir = root_dir + category
    files = glob.glob(image_dir + "/" + "*.jpg")
    print(image_dir + "/" + "*.jpg")
    # print(files)
    for i, f in enumerate(files):  # enumerate 수행 시 idx, data 반환   13만장, 5만장, 9만장
        # 이미지 로딩 (3)
        img = Image.open(f)
        img = img.convert("RGB")
        img = img.resize((img_len, img_len))
        data = np.asarray(img)
        X.append(data)
        Y.append(idx)  # Y에는 해당 이미지가 들어있는 폴더의 인덱스 번호 저장 ex) chicken = 0, dolsotbab = 1, ...

X = np.array(X)
Y = np.array(Y)

# 학습 데이터와 테스트 데이터 나누기 (4)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y)

xy = (X_train, X_test, Y_train, Y_test)

np.save(root_dir + "fashion.npy",xy)
