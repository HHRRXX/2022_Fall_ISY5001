import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator
from keras.models import load_model
import cv2
from PIL import Image
import numpy as np

def detect(img):
    model = load_model('models/cnn.h5')
    img = np.array(img.resize((256,256)))
    imgl = []
    imgl.append(np.array(img))
    x = np.asarray(imgl)

    predict = model.predict(x)
    labels = np.argmax(predict, axis=-1)
    if labels == 0:
        return 'Biographies & Memoirs'
    elif labels == 1:
        return 'Literature & Fiction'
    elif labels == 2:
        return 'Mystery, Thriller & Suspense'
    elif labels == 3:
        return 'Science Fiction & Fantasy'
    elif labels == 4:
        return 'Teen & Young Adult'
#img = Image.open('img/6162592.jpg')
#print(genre(img))
