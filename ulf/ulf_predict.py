
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
from keras.models import load_model
from PIL import Image
import numpy as np

def ulf_total():
    image_files = ['camera.png']
    #image_files = ['denim_skirt.jpg']

    image_size = 64
    nb_classes = len(image_files)
    categories = ["한 벌 옷", "하의", "상의"]

    X = []
    files = []

    for fname in image_files:
        img = Image.open(fname)
        img = img.crop((270,6,950,720))
        img = img.convert("RGB")
        img = img.resize((image_size, image_size))
        in_data = np.asarray(img)
        in_data = in_data.astype("float") / 256
        X.append(in_data)
        files.append(fname)

    X = np.array(X)

    model = load_model('ulf_cropped.h5')
    #model = load_model('model/6layer_ulf_cl_01.h5')

    pre = model.predict(X)

    for i, p in enumerate(pre):
        y = p.argmax()
        print("input:", files[i])
        print("output", "[", y,"]", categories[y], "/ score",p[y])
 
    text = categories[y]
    #print(text)
    return text  
    #print("input: ", files[0]) 
    #print("predict: ", "[",y,"]","/ Score", pre[0][y])

'''
txt_total = []
s = categories[y]
txt = "Type of clothes you choose is " + s 
txt_total.append(txt)
f = open("model_ulf_predict_new.txt", "w")
f.write(txt + '\n')
f.close()
'''
ulf_total()
