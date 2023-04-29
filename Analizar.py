import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import cv2

# cargar el modelo
#model = load_model('modelo.h5')

# Cargar el modelo
model = load_model('modelo.h5')
#model = tf.keras.models.load_model('modelo.h5')

# cargar la imagen que quieres analizar
img = cv2.imread('imagen.jpeg')

# preprocesar la imagen
img = cv2.resize(img, (150, 150))
img_array = np.expand_dims(img, axis=0) / 255.

print("img_array\n",img_array)

# realizar la predicción
predicciones = model.predict(img_array)

# imprimir las predicciones
print(predicciones)