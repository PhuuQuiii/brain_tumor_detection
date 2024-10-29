import numpy as np
import tensorflow as tf
from keras.preprocessing import image

def LoadModel(path):
    return tf.keras.models.load_model(path)



def LoadImage(path):
    img = image.load_img(path, target_size=(224, 224), color_mode='rgb')

    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    return img_array
    

def Prediction(img_array, model):
    pre = model.predict(img_array)
    return {
        "glioma": pre[0][0],
        "meningioma": pre[0][1],
        "notumor": pre[0][2],
        "pituitary": pre[0][3]
    }