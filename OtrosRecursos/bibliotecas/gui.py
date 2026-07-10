import tkinter as tk
from tkinter import Toplevel, ttk
def nuevo():
    ventana1 = Toplevel(ventana)
    ventana1.title("Hola")
    texto = nombre.get()
    ttk.Label(ventana1,text=texto).grid(column=0,row=0)
ventana = tk.Tk()
ventana.title("Hola")
ttk.Label(ventana,text="texto").grid(column=0,row=0)
accion = ttk.Button(ventana,text="soy un botón", command=nuevo).grid(column=1,row=0)
nombre = tk.StringVar()
cajadetexto= ttk.Entry(ventana,width=20,textvariable=nombre).grid(column=0,row=1)
ventana.mainloop()
