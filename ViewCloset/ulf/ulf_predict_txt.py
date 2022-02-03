#-*- coding: utf-8 -*-

import numpy as np
from PIL import Image
from keras.models import load_model

# 테스트 이미지 목록 (1)
image_files = ["./test_img/full1.jpg"]
image_size = 64
nb_classes = len(image_files)
categories = ["한 벌 옷", "하의", "상의"]

X = []
files = []

# 이미지 불러오기 (2)
for fname in image_files:
    img = Image.open(fname)
    img = img.convert("RGB")
    img = img.resize((image_size, image_size))
    in_data = np.asarray(img)
    in_data = in_data.astype("float") / 256
    X.append(in_data)
    files.append(fname)

X = np.array(X)

# 모델 파일 읽어오기  (3)   model_early_test_08.h5 = 4층 신경망 + Dropout 0.3 + Global Max Pooling
model = load_model('../DeepFashion/attribute_predict/up_down/fashion_model_early_test_08.h5')

# 예측 실행  (4)
pre = model.predict(X)
y = pre.argmax()

print("입력:", files[0])
print("예측:", "[",y,"]",categories[y],"/ Score",pre[0][y])

s = categories[y]
txt = "당신이 고른 의상은 " + s + " 입니다."

# print(txt)
f = open("model_ulf_predict.txt","w")
f.write(txt + "\n")
f.close()

'''
# 예측 결과 출력 (5)
for i, p in enumerate(pre):
   y = p.argmax()   #  원 핫 인코딩을 통해 얻은 데이터들 중 가장 큰 값의 데이터 반환
   print(y)
   print("o:",p)
   print("pre:",pre)
   print("입력:", files[i])    # 정답
   print("예측:", "[", y, "]", categories[y], "/ Score",p[y])
'''