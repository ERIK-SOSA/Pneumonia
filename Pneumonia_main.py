import tensorflow as tf
#from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import h5py

print("\nVersion de Tensorflow\n",tf.__version__)

# Definir los parámetros del modelo
input_shape = (150, 150, 3)
batch_size = 32
num_classes = 2
epochs = 5

# Crear un objeto ImageDataGenerator para hacer el preprocesamiento de las imágenes
train_datagen = ImageDataGenerator(rescale=1./255)

print("\ntrain_datagen\n",train_datagen,"\n")

# Cargar el conjunto de entrenamiento
train_generator = train_datagen.flow_from_directory(
        'chest_xray/train',
        target_size=input_shape[:2],
        batch_size=batch_size,
        class_mode='categorical')

# Definir la arquitectura del modelo CNN
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

# Compilar el modelo
model.compile(optimizer='nadam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Entrenar el modelo
model.fit(train_generator, epochs=epochs)

# print("")
# print("")

# # Cargar el conjunto de validación
# validation_datagen = ImageDataGenerator(rescale=1./255)

# validation_generator = validation_datagen.flow_from_directory(
#         'chest_xray/val',
#         target_size=input_shape[:2],
#         batch_size=batch_size,
#         class_mode='categorical')

# # Evaluar el modelo en el conjunto de validación
# evaluation = model.evaluate(validation_generator)

# # Imprimir la precisión y la pérdida
# print('Accuracy:', evaluation[1])
# print('Loss:', evaluation[0])



# Guardar el modelo
model.save('modelo.h5')

#tf.saved_model.save(model,'modelotf')