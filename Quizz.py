from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import subprocess
import random
import os

ruta_imagen = ""
puntos = 0
cont = 0

class QuizzApp:
  
    def __init__(self, master):
        self.master = master
        master.title("Quizz")
        ### Crear el diseño de la aplicación ###
        
        # Boton Regresar
        self.boton_regresar = Button(root, text="Regresar", font=("Arial", 10), command=self.regresar,  bg='#17897a', fg='#ffffff')
        self.boton_regresar.pack(side="bottom", anchor="ne", pady=10, padx=10)

        # Etiqueta de titulo
        self.etiqueta_titulo = Label(root, text="Quizz", font=("Arial", 28), bg="#000000", fg="#e0dddd", bd=2, justify=CENTER, relief=FLAT, cursor="sizing")
        self.etiqueta_titulo.place(x=100,y=10,width=310,height=82)

        # Etiqueta de puntos
        self.etiqueta_puntos = Label(root, font=("Arial", 13), bg="#779F0C", fg="#9F0C0C", bd=2, justify=CENTER, relief=FLAT, cursor="sizing")
        self.etiqueta_puntos.place(x=410,y=10,width=90,height=82)

        # Etiqueta de instrucciones
        self.instrucciones = Label(root, text="En este apartado podras poner a prueba tus \nconocimientos analizando imagenes de rayos x.", font = ('Times', 10), fg="#333333", justify="center")
        self.instrucciones.place(x=100,y=102,width=400,height=40)

        # Boton para cargar una imagen random
        # self.boton_cargar_imagen= Button(root, text="Cargar imagen", font=('Times',10), command=self.inicio, bg="#f10c0c", fg="#fbfbfb")
        # self.boton_cargar_imagen.place(x=150,y=152,width=300,height=30)

        # Boton para restablecer valores originales y practicar nuevamente
        self.practicar_denuevo_button = Button(root, text="Practicar de nuevo", font=('Times',10), command=self.play_again, bg="#f10c0c", fg="#fbfbfb")
        self.practicar_denuevo_button.place(x=150,y=152,width=300,height=30)

        # Etiqueta donde se muestra la imagen random
        self.etiqueta_imagen = Label(root, fg="#ffffff")
        self.etiqueta_imagen.place(x=150,y=192,width=300,height=300)

        # Etiqueta de instrucciones
        self.instrucciones2 = Label(root, text="Según tu analisís la imagen de rayos x \nes positivo o negativo para neumonía.", font = ('Times', 10), fg="#333333", justify="center")
        self.instrucciones2.place(x=100,y=502,width=400,height=40)

        # Variable asociada a los radiobuttons
        self.radio_var = StringVar()
        self.radio_var.set(None) # Ningún botón seleccionado por defecto

        # # Radio boton positivo
        self.radio_boton_positivo = Radiobutton(root, text="POSITIVO", font = ('Times',10), fg="#f11818", bg="#14a214", justify="center", variable=self.radio_var, value="Positivo", command=...)
        self.radio_boton_positivo.place(x=150,y=552,width=85,height=25)

        # # Radio boton negativo
        self.radio_boton_negativo = Radiobutton(root, text="NEGATIVO", font=('Times',10), fg="#2030b0", bg="#14a214", justify="center", variable=self.radio_var, value="Negativo", command=...)
        self.radio_boton_negativo.place(x=250,y=552,width=85,height=25)

        # Boton para comprobar la respuesta
        self.boton_comprobar = Button(root, text="Comprobar", font=('Times', 10), command=self.mostrar_resultado, bg="#0A5460", fg="#ffffff", justify="center")
        self.boton_comprobar.place(x=350,y=552,width=100,height=25)

        # Etiqueta para mostrar el resultado de la seleccion
        self.etiqueta_respuesta = Label(root, font=('Times',25), fg="#333333", bg="#14a019", justify="center")
        self.etiqueta_respuesta.place(x=100,y=587, width=400, height=100)
        # etiqueta_respuesta.pack(pady=430)

    # Función para verificar la respuesta del usuario
    def mostrar_resultado(self):

        seleccion = self.radio_var.get() # Obtener la opción seleccionada

        global ruta_imagen
        global puntos
        global cont

        if ruta_imagen == "":
            self.etiqueta_respuesta.config(text="Cargar una imagen \nantes de empezar")

        # Cargar el modelo
        model = load_model('pneumonia_model.h5')

        # Cargar la imagen que quieres analizar
        img = cv2.imread(ruta_imagen)

        # Preprocesar la imagen
        img = cv2.resize(img, (150, 150))
        img_array = np.expand_dims(img, axis=0) / 255.

        # Realizar la predicción
        predicciones = model.predict(img_array)

        if seleccion == "Positivo":
            # self.etiqueta_respuesta.config(text="Seleccionaste Positivo")
            if predicciones[0][0] > predicciones[0][1]:
                self.etiqueta_respuesta.config(text="Respuesta incorrecta")
                puntos -= 10
                self.etiqueta_puntos.config(text=f"Puntos: {puntos}")
                self.restablecer_radiobuttons()
                cont += 1
                if cont == 9:
                    # self.boton_cargar_imagen.config(state=DISABLED)
                    self.boton_comprobar.config(state=DISABLED)
                    self.radio_boton_positivo.config(state=DISABLED)
                    self.radio_boton_negativo.config(state=DISABLED)
                    self.etiqueta_respuesta.config(text=f"Has completado las 10 rondas.\nTu punteo es de: {puntos}")
                elif cont < 9:
                    self.inicio()
            else: 
                self.etiqueta_respuesta.config(text="Respuesta correcta")
                puntos += 10
                self.etiqueta_puntos.config(text=f"Puntos: {puntos}")
                self.restablecer_radiobuttons()
                cont += 1
                if cont == 9:
                    # self.boton_cargar_imagen.config(state=DISABLED)
                    self.boton_comprobar.config(state=DISABLED)
                    self.radio_boton_positivo.config(state=DISABLED)
                    self.radio_boton_negativo.config(state=DISABLED)
                    self.etiqueta_respuesta.config(text=f"Has completado las 10 rondas.\nTu punteo es de: {puntos}")
                elif cont < 9:
                    self.inicio()
            
        elif seleccion == "Negativo":
            # self.etiqueta_respuesta.config(text="Seleccionaste Negativo")
            if predicciones[0][0] < predicciones[0][1]:
                self.etiqueta_respuesta.config(text="Respuesta incorrecta")
                puntos -= 10
                self.etiqueta_puntos.config(text=f"Puntos: {puntos}")
                self.restablecer_radiobuttons()
                cont += 1
                if cont == 9:
                    # self.boton_cargar_imagen.config(state=DISABLED)
                    self.boton_comprobar.config(state=DISABLED)
                    self.radio_boton_positivo.config(state=DISABLED)
                    self.radio_boton_negativo.config(state=DISABLED)
                    self.etiqueta_respuesta.config(text=f"Has completado las 10 rondas.\nTu punteo es de: {puntos}")
                elif cont < 9:
                    self.inicio()
            else: 
                self.etiqueta_respuesta.config(text="Respuesta correcta")
                puntos += 10
                self.etiqueta_puntos.config(text=f"Puntos: {puntos}")
                self.restablecer_radiobuttons()
                cont += 1
                if cont == 9:
                    # self.boton_cargar_imagen.config(state=DISABLED)
                    self.boton_comprobar.config(state=DISABLED)
                    self.radio_boton_positivo.config(state=DISABLED)
                    self.radio_boton_negativo.config(state=DISABLED)
                    self.etiqueta_respuesta.config(text=f"Has completado las 10 rondas.\nTu punteo es de: {puntos}")
                elif cont < 9:
                    self.inicio()
                
        else:
            self.etiqueta_respuesta.config(text="Debes seleccionar una opción")
            pass
        print("Cont >> ", cont)


    def play_again(self):
        global ruta_imagen
        global puntos
        global cont
        
        ruta_imagen = ""
        puntos = 0
        cont = 0
        
        self.restablecer_radiobuttons()
        self.etiqueta_puntos.config(text=f"Puntos: {puntos}")
        self.etiqueta_respuesta.config(text="")
        self.boton_comprobar.config(state=NORMAL)
        self.radio_boton_positivo.config(state=NORMAL)
        self.radio_boton_negativo.config(state=NORMAL)
        
        self.inicio()
        
    # Función para regresar a la ventana principal
    def regresar(self):
        subprocess.Popen(['python', 'Analizador.py'])
        root.withdraw()

    # Función para cargar una imagen random
    def cargar_imagen(self):
        global ruta_imagen  # Obtener la referencia a la variable global
        ruta_carpeta = "quizz"
        lista_archivos = os.listdir(ruta_carpeta)
        archivo_seleccionado = random.choice(lista_archivos)
        lista_archivos = list(filter(lambda archivo: archivo.endswith('.jpeg'), os.listdir(ruta_carpeta)))
        ruta_imagen = ruta_carpeta+"/"+archivo_seleccionado
        imagen = Image.open(ruta_imagen)
        imagen = imagen.resize((300,300), Image.ANTIALIAS)
        imagen_referencia = ImageTk.PhotoImage(imagen)
        self.etiqueta_imagen.configure(image=imagen_referencia)
        self.etiqueta_imagen.image = imagen_referencia  # Asignar la imagen a la etiqueta
        # print(f"El archivo seleccionado al azar es: {archivo_seleccionado}")

    def inicio(self):
        self.cargar_imagen()

    def restablecer_radiobuttons(self):
        self.radio_var.set(None)

# Configuración de la ventana principal
root = tk.Tk()

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
root.title("Quizz")
# root.geometry("600x650")
root.resizable(False, False)
# root.resizable(True, True)
root.configure(bg='#14a214')

app = QuizzApp(root)

if cont < 9:
    app.inicio()
    # print(i)
app.etiqueta_puntos.config(text=f"Puntos: {puntos}")
print("Cont >> ", cont)

root.mainloop()
