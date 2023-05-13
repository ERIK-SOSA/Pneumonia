from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import cv2

import subprocess

ruta_imagen = ""

# Función que carga la imagen seleccionada
def cargar_imagen():
    global ruta_imagen, imagen_referencia  # Obtener la referencia a las variables globales
    ruta_imagen = filedialog.askopenfilename(initialdir = "/", title = "Seleccionar imagen", filetypes = (("Archivos JPEG", "*.jpeg"), ("Archivos PNG", "*.png"), ("Archivos JPG", "*.jpg"), ("Todos los archivos", "*.*")))
    print ("ruta_imagen", ruta_imagen)
    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((300, 300), Image.ANTIALIAS)
    imagen_referencia = ImageTk.PhotoImage(imagen)
    etiqueta_imagen.configure(image=imagen_referencia)
    etiqueta_imagen.image = imagen_referencia  # Asignar la imagen a la etiqueta

# Función que analiza la imagen seleccionada
def analizar_imagen():
    global ruta_imagen  # Obtener la referencia a la variable global
    if ruta_imagen == "":
        resultado_analisis.config(text="No se ha seleccionado \nninguna imagen.")
        return
    
    # Cargar el modelo
    model = load_model('pneumonia_model.h5')

    # Cargar la imagen que quieres analizar
    img = cv2.imread(ruta_imagen)

    # Preprocesar la imagen
    img = cv2.resize(img, (150, 150))
    img_array = np.expand_dims(img, axis=0) / 255.

    # Realizar la predicción
    predicciones = model.predict(img_array)

    # Imprimir las predicciones
    # print(predicciones)

    # print("\n")

    # Imprimir el resultado de la predicción
    if predicciones[0][0] > predicciones[0][1]:
        resultado_analisis.config(text="La imagen de rayos X \nNo tiene neumonía.")
        # print("La imagen de rayos X NO tiene neumonía.")

    else:
        resultado_analisis.config(text="La imagen de rayos X \nSí tiene neumonía.")
        # print("La imagen de rayos X SÍ tiene neumonía.")

# Función que reinicia la ventana
def restablecer_ventana():
    global ruta_imagen
    etiqueta_imagen.config(image="")
    ruta_imagen = ""
    resultado_analisis.config(text="")

# Función para entrenar estudiantes    
def quizz():
    #root.withdraw()
    subprocess.Popen(['python', 'Quizz.py'])
    root.withdraw()

# Configuración de la ventana principal
root = Tk()

# Obtener las dimensiones de la pantalla
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()

# Dimensiones de la ventana
ancho_ventana = 600
alto_ventana = 700

# Calcular las coordenadas para centrar la ventana
x = int(ancho_pantalla/2 - ancho_ventana/2)
y = int(alto_pantalla/2 - alto_ventana/2)

# Configurar la posición de la ventana
root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
root.title("Análisis de neumonía con inteligencia artificial")
# root.geometry("600x650")
root.resizable(False, False)
# root.resizable(True, True)
root.configure(bg='#17897a')

# Boton Quizz
boton_quizz = Button(root, text="Quizz", font=("Arial", 10), command=quizz, bg='#14a214', fg='#ffffff')
boton_quizz.place(x=545, y=660 , width=45, height=30)

# Etiqueta de titulo
etiqueta_titulo = Label(root, bg="#060606", font=('Times', 28), fg="#ffffff", justify="center", text="Detector de Neumonía")
etiqueta_titulo.place(x=155, y=20, width=390, height=82)

# Cargar la imagen
icono = Image.open("icono.png")
icono = icono.resize((100,82), Image.ANTIALIAS)

# Convertir la imagen a un formato compatible con tkinter
imagen_tk = ImageTk.PhotoImage(icono)

# Etiqueta icono
etiqueta_icono = Label(root, font=('Times', 10), fg="#333333", bg="#060606", justify="center", image=imagen_tk, text="icono")
etiqueta_icono.place(x=55, y=20, width=100, height=82)

# Botón para cargar imagen
boton_cargar_img = Button(root, activebackground="#2ee621", activeforeground="#95be65", bg="#11c463", command=cargar_imagen, cursor="sizing", disabledforeground="#cc0000", font=('Times', 10), fg="#ffffff", justify="center", text="Cargar Imagen ", relief="groove")
boton_cargar_img.place(x=150, y=130, width=300, height=30)

# Botón para analizar imagen
boton_analizar = Button(root, bg="#1e9fff", command=analizar_imagen, font=('Times', 10), fg="#ffffff", justify="center", text="Analizar")
boton_analizar.place(x=150, y=170, width=300, height=30)

# Botón para restablecer la ventana
boton_restablecer = Button(root, bg="#d62222", command=restablecer_ventana, font=('Times', 10), fg="#ffffff", justify="center", text="Restablecer")
boton_restablecer.place(x=150, y=210, width=300, height=30)

# Etiqueta para mostrar la imagen seleccionada
etiqueta_imagen = Label(root, font=('Times', 10), bg="#17897a", justify="center")
etiqueta_imagen.place(x=150, y=270, width=300, height=300)

# Etiqueta para mostrar el resultado del análisis
resultado_analisis = Label(root, font=('Times', 25), bg="#17897a", justify="center")
resultado_analisis.place(x=150, y=580, width=300, height=100)

root.mainloop()