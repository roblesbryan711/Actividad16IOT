from tkinter import *
from PIL import Image, ImageTk
import serial

try:
    arduino = serial.Serial('COM4', 9600)
except:
    print("Verifica el puerto serial")
    exit()

def girarizquierda():
    boton1.config(state=DISABLED)
    boton2.config(state=NORMAL)
    boton3.config(state=NORMAL)
    mensaje.config(image=giroizquierda)
    arduino.write(b'i')


def detenermotor():
    boton1.config(state=NORMAL)
    boton2.config(state=DISABLED)
    boton3.config(state=NORMAL)
    mensaje.config(image=motorparado)
    arduino.write(b'p')

def girarderecha():
    boton1.config(state=NORMAL)
    boton2.config(state=NORMAL)
    boton3.config(state=DISABLED)
    mensaje.config(image=giroderecha)
    arduino.write(b'd')
    
    
ventana = Tk()
ventana.title("Control del Motor de corriente directa")
ventana.geometry("1200x1200")
giroizquierda = ImageTk.PhotoImage(Image.open("giroalaizquierda.png"))
motorparado = ImageTk.PhotoImage(Image.open("motorparado.jpg"))
giroderecha = ImageTk.PhotoImage(Image.open("giroaladerecha.png"))
izquierda = ImageTk.PhotoImage(Image.open("flechaizquierda.png"))
detener = ImageTk.PhotoImage(Image.open("detener.jpg"))
derecha = ImageTk.PhotoImage(Image.open("flechaderecha.jpg"))
boton1 = Button(ventana, image=izquierda, bg="green", command=girarizquierda)
boton2 = Button(ventana, image=detener, bg="green", state=DISABLED, command=detenermotor) 
boton3 = Button(ventana, image=derecha, bg="green", command=girarderecha)
boton1.place(x=10, y=10)
boton2.place(x=300, y=10)
boton3.place(x=700, y=10)
mensaje = Label(ventana, image=motorparado)
mensaje.place(x=10, y=350)
#esta linea siempre va al final
ventana.mainloop() 
arduino.write(b'p')
arduino.close()



