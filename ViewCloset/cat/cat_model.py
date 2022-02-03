#-*- coding: utf-8 -*-
## 사용할 모델 라이브러리 import

import sys, os
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Activation
from keras.layers import Dropout
from keras.layers import GlobalMaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.utils import np_utils
from keras.callbacks import EarlyStopping

import numpy as np
import matplotlib.pyplot as plt

# save np.load
np_load_old = np.load

# modify the default parameters of np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

early_stopping_callback = EarlyStopping(monitor='val_loss',patience=10)

f = open('../../DeepFashion/attribute_predict/anno/list_category_cloth.csv','r')

path = '../../DeepFashion/attribute_predict/category/'

types = []; cat = []; tmp_cat = []; cat_name = []

while(True):
    lines = f.read().splitlines()   # ['Anorak,1', 'Blazer,1', 'Blouse,1', ... , 'Sundress,3']

    if not lines:
        break

    for i, d in enumerate(lines):
        tmp = lines[i]      # 'Anorak,1'
        num_index = len(lines[i]) - 2
        tmp_cat = tmp[:num_index]   # 'Anorak'
        cat.append(tmp_cat)


nb_classes = len(cat)
image_size = 64

# 데이터 로딩  (1)
def load_dataset():
    x_train, x_test, y_train, y_test = np.load("../../DeepFashion/attribute_predict/category/cat_graph.npy")
    x_train = x_train.astype("float") / 256
    x_test = x_test.astype("float") / 256
    y_train = np_utils.to_categorical(y_train, nb_classes)
    y_test = np_utils.to_categorical(y_test, nb_classes)
    return x_train, x_test, y_train, y_test


# 모델 구성  (2)
def build_model(in_shape):
    model = Sequential()
    model.add(Convolution2D(16, 3, 3, border_mode='Same',
                            input_shape=in_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.30))
    model.add(Convolution2D(32, 3, 3, border_mode='Same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.30))
    model.add(Convolution2D(64, 3, 3, border_mode='Same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.30))
    model.add(Convolution2D(128, 3, 3, border_mode='Same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.30))
    model.add(Convolution2D(196,3, 3, border_mode='Same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Convolution2D(256, 3, 3, border_mode='Same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.30))
    model.add(GlobalMaxPooling2D(data_format="channels_last"))
    model.add(Dropout(0.30))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model


# 모델 평가하기  (4)
def model_eval(model, x, y):
    score = model.evaluate(x, y)
    print('loss=', score[0])
    print('accuracy=', score[1])


# 모델 학습 및 평가 (학습 중단점 지정)
x_train, x_test, y_train, y_test = load_dataset()

model = build_model(x_train.shape[1:])
history = model.fit(x_train, y_train, validation_data=(x_test, y_test), batch_size=30, epochs=180,callbacks=[early_stopping_callback])

y_acc = history.history['accuracy']
y_vacc = history.history['val_accuracy']
y_loss = history.history['loss']
y_vloss = history.history['val_loss']

x_len = np.arange(len(y_acc))

plt.plot(x_len, y_acc, marker=".", c="blue", label='Trainset_accuracy')
plt.plot(x_len, y_vacc, marker='.', c="red", label='Testset_accuracy')

plt.legend(loc='upper right')
# plt.axis([0, 20, 0, 0.35])
plt.grid()

plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.show()

plt.plot(x_len, y_loss, marker=".", c="blue", label='Trainset_loss')
plt.plot(x_len, y_vloss, marker='.', c="red", label='Testset_loss')

plt.legend(loc='upper right')
# plt.axis([0, 20, 0, 0.35])
plt.grid()

plt.xlabel('epochs')
plt.ylabel('loss')
plt.show()

# verbose = 0 설정하면 수행되는거 안보여!
model_eval(model, x_test, y_test)
model.summary()

# 모델 저장
#model.save("../DeepFashion/attribute_predict/clothes_type/clothes_category_model.h5")
model.save("../../DeepFashion/attribute_predict/category/cat_graph_6layer.h5")
