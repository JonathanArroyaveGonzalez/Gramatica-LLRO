import sys
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from model.gramaticaControl import Gramatica

class Interfaz:

    def __init__(self):
        self.noTerminales = []
        self.terminales = []
        self.terminalesMasNoTerminales = []
        self.gramatica = Gramatica()
        self.ventana = Tk()
        self.ventana.geometry("1200x800")
        self.imagen_fondo = Image.open("fondo.jpg")
        self.imagen_fondo = self.imagen_fondo.resize((1200, 800), Image.LANCZOS)
        # Convertir la imagen a formato compatible con Tkinter
        self.imagen_fondo_tk = ImageTk.PhotoImage(self.imagen_fondo)
        # Crear el canvas con la imagen de fondo
        self.canvas_principal = Canvas(self.ventana, width=1300, height=800)
        self.canvas_principal.pack()

        # Agregar la imagen de fondo al canvas
        self.canvas_principal.create_image(0, 0, anchor="nw", image = self.imagen_fondo_tk)
        self.image = self.imagen_fondo_tk
        self.canvas_principal.place(x=0, y=0)

        #canvas_principal.create_image(ventana, width=1350, image="fondo.jpg")

        self.lblGramatica = Label(self.canvas_principal, fg="white", bg="#3A91A6", width=18, text="Gramática",
                                  font=("Arial", 17))
        self.lblGramatica.place(x=50, y=20)

        self.textGramatica = scrolledtext.ScrolledText(
            self.ventana, wrap=tk.WORD, width=23, height=10, font=("Arial", 15))
        self.textGramatica.grid(column=0, row=0, padx=40, pady=60)
        self.textGramatica.focus()

        self.lblGramatica2 = Label(self.canvas_principal, fg="white", bg="#3A91A6", width=18, text="Producciones R",
                            font=("Arial", 17)).place(x=390, y=20)

        self.lstGramaticaLeida = scrolledtext.ScrolledText(self.ventana, fg="black", bg="white", width=35, height=15, font=(
            "Arial", 10), relief="solid", highlightbackground="white", highlightthickness=2)
        self.lstGramaticaLeida.place(x=380, y=60)

        self.lblEstados = Label(self.canvas_principal, fg="white", bg="#3A91A6", width=18, text="Estados",
                            font=("Arial", 17)).place(x=730, y=20)

        self.lstEstados = scrolledtext.ScrolledText(self.ventana, fg="black", bg="white", width=35, height=35, font=(
            "Arial", 10), relief="solid", highlightbackground="white", highlightthickness=2)
        self.lstEstados.place(x=720, y=60)

        self.lblTransiciones = Label(self.canvas_principal, fg="white", bg="#3A91A6", width=18, text="Transiciones",
                                     font=("Arial", 17))
        self.lblTransiciones.place(x=390, y=360)

        self.lstTransiciones = scrolledtext.ScrolledText(self.ventana, fg="black", bg="white", width=35, height=15, font=(
            "Arial", 10), relief="solid", highlightbackground="white", highlightthickness=2)
        self.lstTransiciones.place(x=380, y=400)

        self.btn_Iniciar = Button(self.ventana, fg="white", bg="green", width=15, text="Iniciar", state="normal", font=("Arial", 10),
                     command=self.iniciarPrograma)
        self.btn_Iniciar.place(x=40, y=310)

        self.btn_Salir = Button(self.canvas_principal, fg="white", bg="red", width=15, text="Terminar", font=("Arial", 10),
                        command=sys.exit).place(x=185, y=310)

        # Mostrar la gramática leída
    def mostrarGramaticaLeida(self):
        self.lstGramaticaLeida.delete(1.0, END)
        for gram in self.gramatica.gramaticaLeida:
            self.lstGramaticaLeida.insert(END, "\n\n " + gram)
        self.lstGramaticaLeida.configure(state='disabled')

    def mostrarEstados(self):
        self.lstEstados.delete(1.0, END)
        for i in range(len(self.gramatica.estados)):
            self.lstEstados.insert(END, "\n\n Estado-I{0}: {1}".format(i, self.gramatica.estados[i]))
        self.lstEstados.configure(state='disabled')

    def mostrarEstadosConPunto(self):
        self.lstGramaticaLeida.delete(1.0, END)
        for i, estado in enumerate(self.gramatica.estados):
            producciones = estado
            producciones_con_punto = [p for p in producciones if p.endswith(".")]
            if producciones_con_punto:
                self.lstGramaticaLeida.insert(END, "\n\nEstado-I{0}: {1}".format(i, estado))
                self.lstGramaticaLeida.insert(END, "\nProducciones R:")
                for p in producciones_con_punto:
                    self.lstGramaticaLeida.insert(END, "\n- {0}".format(p))
        self.lstGramaticaLeida.configure(state='disabled')

    #  mostrar transiciones
    def mostrarTransiciones(self):
        self.lstTransiciones.delete(1.0, END)
        for f in self.gramatica.transiciones:
            self.lstTransiciones.insert(
                END, "\n\n Transición (I{0} -> I{2}) = {1}".format(f[0], f[1], f[2]))
        self.lstTransiciones.configure(state='disabled')

    def leerGramatica(self):
        gram = self.textGramatica.get(1.0, END).split('\n')
        gram.remove('')

        for linea in gram:
            lineaLimpia = linea.replace(" ", "")
            self.gramatica.gramaticaLeida.append(lineaLimpia)

    # Iniciar el Programa, lo activa el boton "iniciar"
    def iniciarPrograma(self):
        if len(self.textGramatica.get(1.0, END)) == 1:
            messagebox.showerror(message="Gramatica Vacía", title="Error")
        else:
            self.btn_Iniciar["state"] = "disabled"
            self.leerGramatica()
            #self.mostrarGramaticaLeida()
            self.gramatica.dividirTerminalesYNoTerminales()
            self.gramatica.agregarPunto()
            self.gramatica.obtenerEstados()
            self.mostrarEstados()
            self.mostrarTransiciones()
            self.gramatica.esLR0()
            self.mostrarEstadosConPunto()
        

    def ejecutar(self):
            self.ventana.mainloop()