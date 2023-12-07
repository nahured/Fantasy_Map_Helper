from PIL import Image,ImageTk
import tkinter as tk
from tkinter import filedialog,messagebox

# Modulo propio
from calculadoras import skcc
from calculadoras import MapaAltura



class Biomas():
    def __init__(self,root):
        self.root = root
        self.mapa_temperatura_inicio = ""
        self.mapa_temperatura_mitad = ""
        self.mapa_presipitacion_inicio = ""
        self.mapa_presipitacion_mitad = ""

    def abrir_mapa_temperatura_inicio(self):
        img = filedialog.askopenfilename(title="Abrir mapa de temperatura al principio del año",filetypes=[("mapa temperatura",".png")])
        comp =skcc.verificar_color("t",img)
        if comp:
            messagebox.showerror("color invalido",f"en el pixel {comp[0]} el color no es correcto con R={comp[1][0]} G={comp[1][1]} B={comp[1][2]}")
            self.mapa_temperatura_inicio = img
        else:
            self.mapa_temperatura_inicio = img
    
    def abrir_mapa_temperatura_mitad(self):
        img = filedialog.askopenfilename(title="Abrir mapa de temperatura al mitad del año",filetypes=[("mapa temperatura",".png")])
        comp =skcc.verificar_color("t",img)
        if comp:
            messagebox.showerror("color invalido",f"en el pixel {comp[0]} el color no es correcto con R={comp[1][0]} G={comp[1][1]} B={comp[1][2]}")
            self.mapa_temperatura_mitad = img
        else:
            self.mapa_temperatura_mitad = img
    
    def abrir_mapa_presipitacion_inicio(self):
        img = filedialog.askopenfilename(title="Abrir mapa de presipitacion al principio del año",filetypes=[("mapa presipitacion",".png")])
        comp =skcc.verificar_color("p",img)
        if comp:
            messagebox.showerror("color invalido",f"en el pixel {comp[0]} el color no es correcto con R={comp[1][0]} G={comp[1][1]} B={comp[1][2]}")
            self.mapa_presipitacion_inicio = img
        else:
            self.mapa_presipitacion_inicio = img
    
    def abrir_mapa_presipitacion_mitad(self):
        img = filedialog.askopenfilename(title="Abrir mapa de presipitacion al mitad del año",filetypes=[("mapa presipitacion",".png")])
        comp =skcc.verificar_color("p",img)
        if comp:
            messagebox.showerror("color invalido",f"en el pixel {comp[0]} el color no es correcto con R={comp[1][0]} G={comp[1][1]} B={comp[1][2]}")
            self.mapa_presipitacion_mitad = img
        else:
            self.mapa_presipitacion_mitad = img
    
    def guardar_mapa(self):
        guardar_mapa = filedialog.asksaveasfilename(title="Guardar el mapa climatologico de Koppen",defaultextension=".png")
        if (self.mapa_temperatura_inicio != "" and self.mapa_temperatura_mitad != "" and self.mapa_presipitacion_inicio != "" and self.mapa_presipitacion_mitad != "") == True:
            imagen_bioma = skcc.koppen(self.mapa_temperatura_inicio,self.mapa_temperatura_mitad,self.mapa_presipitacion_inicio,self.mapa_presipitacion_mitad)
            imagen_bioma.save(guardar_mapa)
            messagebox.showinfo("Terminado",f"La imagen se guardo correctamente en {guardar_mapa}")
    



    def ventana(self):
        bioma_ventana = tk.Toplevel(self.root)
        bioma_ventana.title("climas de Koppen")
        bioma_ventana.config(bg="gray25")
        bioma_ventana.geometry("280x130")
        bioma_ventana.resizable(width=False, height=False)
        

        boton_temperatura_inicio = tk.Button(bioma_ventana,text="temperatura al principio del año",command=self.abrir_mapa_temperatura_inicio,bg="gray35").pack(side="top")
        boton_temperatura_mitad = tk.Button(bioma_ventana,text="temperatura a la mitad del año",command=self.abrir_mapa_temperatura_mitad,bg="gray35").pack(side="top")
        boton_presipitacion_inicio = tk.Button(bioma_ventana,text="precipitacion al principio del año",command=self.abrir_mapa_presipitacion_inicio,bg="gray35").pack(side="top")
        boton_presipitacion_mitad = tk.Button(bioma_ventana,text="precipitacion a la mitad del año",command=self.abrir_mapa_presipitacion_mitad,bg="gray35").pack(side="top")
        boton_guardar = tk.Button(bioma_ventana,text="guardar mapa",command=self.guardar_mapa,bg="gray35").pack(side="top")
        bioma_ventana.lift()



class Sombra_de_lluvia():
    def __init__(self,root):
        self.root = root
        self.mapa_altura_imagen = ""
    
    def abrir_mapa_altura(self):
        self.mapa_altura_imagen = filedialog.askopenfilename(title="Abrir mapa de altura",filetypes=[("mapa altura",".png")])
    
    def guardar_mapa(self):
        guardar_sombra_lluvia_imagen = filedialog.asksaveasfilename(title="guardar mapa sombra de lluvia",defaultextension=".png")
        if self.mapa_altura_imagen:
            img = MapaAltura.sombra_de_lluvia(self.mapa_altura_imagen,21.287,50,6371000.0)
            img.save(guardar_sombra_lluvia_imagen)
            messagebox.showinfo("Terminado",f"La imagen se guardo correctamente en {guardar_sombra_lluvia_imagen}")
    

    def ventana(self):
        sombra_lluvia = tk.Toplevel(self.root)
        sombra_lluvia.title("Sombra de lluvia")
        sombra_lluvia.config(bg="gray25")
        sombra_lluvia.geometry("280x130")
        sombra_lluvia.resizable(width=False, height=False)
        

        boton_mapa_altura = tk.Button(sombra_lluvia,text="Mapa de altura",command=self.abrir_mapa_altura,bg="gray35").pack(side="top")
        boton_guardar_mapa = tk.Button(sombra_lluvia,text="guardar mapa sombra de lluvia",command=self.guardar_mapa,bg="gray35").pack(side="top")
        sombra_lluvia.lift()



def ventana_principal():

    root = tk.Tk() # ventana principal

    root.title("Mapa de Fantasia")
    root.config()
    ancho_alto = f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}"
    root.geometry(ancho_alto) # tamaño inicial de la ventana
    root.state('zoomed')


    label1 = tk.Frame(root) #Menu de obciones
    label1.config(bg="gray25")
    label2 = tk.Frame(root) #barra de herramientas
    label2.config(bg="gray25")

    label3 = tk.Frame(root) # visor
    label3.config(bg="gray28")
    label4 = tk.Frame(root) # menu de edicion
    label4.config(bg="gray25")

    # Redimensionar la cuadrícula (grid)
    root.columnconfigure(0, weight=1)  # Ajustar la columna 0
    root.columnconfigure(1, weight=9)  # Ajustar la columna 1
    root.columnconfigure(2, weight=2)  # Ajustar la columna 1
    root.rowconfigure(0, weight=2)     # Ajustar la fila 0
    root.rowconfigure(1, weight=20)     # Ajustar la fila 1

    # Usar el método grid para ubicar las etiquetas en el grid
    label1.grid(row=0, column=0,columnspan=3,sticky="nsew")  # sticky="nsew" para que se expandan con la ventana
    label2.grid(row=1, column=0, sticky="nsew")
    label3.grid(row=1, column=1, sticky="nsew")
    label4.grid(row=1, column=2, sticky="nsew")


    #Barra de Herramientas
    clase_bioma = Biomas(root)
    bioma_imagen = ImageTk.PhotoImage(Image.open("gui\iconos\Biomas.png"))
    boton_bioma = tk.Button(label2,image=bioma_imagen,command=clase_bioma.ventana,bg="gray25")
    boton_bioma.grid(row=0,column=0)

    clase_sombra_lluvia = Sombra_de_lluvia(root)

    sombra_lluvia_imagen = ImageTk.PhotoImage(Image.open("gui\iconos\Sombra_de_lluvia_imagen.png"))
    boton_sombra_lluvia = tk.Button(label2,image= sombra_lluvia_imagen,command=clase_sombra_lluvia.ventana,bg="gray25").grid(row=0,column=1)

    root.mainloop()