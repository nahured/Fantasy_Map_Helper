
import tkinter as tk
from tkinter import filedialog

# Modulos propios
from calculadoras import MapaAltura
from calculadoras import skcc
from gui.ventanas import ventana_principal

#from calculadoras.MapaAltura import Sombra_de_lluvia





def Sombra_lluvia():
    archivo = filedialog.askopenfilename(filetypes=[("imagen del planeta",".png")])
    save = Guardar_archivo()
    if archivo:
        SLLprocesar_archivo(archivo,save)

def Guardar_archivo():
    archivo_guardado = filedialog.asksaveasfilename(defaultextension=".png")

    if archivo_guardado:
        return archivo_guardado

def SLLprocesar_archivo(nombre_archivo,save):
    radio_ecuatorial_tierra = 6371000.0
    alt_max = 8.848 #21.287  la altura maxima de mi mapa de altura que da como resultado a la montaña mas alta que es de 21.3 M
    Alt_viento = 20
    MapaAltura.Sombra_de_lluvia(nombre_archivo,alt_max,Alt_viento,radio_ecuatorial_tierra,save)


def Bioma():
    mapa_temperatura =filedialog.askopenfilename(filetypes=[("imagen del planeta",".png")])
    mapa_temperatura_mitad_ano =filedialog.askopenfilename(filetypes=[("imagen del planeta",".png")])
    mapa_predipitacion =filedialog.askopenfilename(filetypes=[("imagen del planeta",".png")])
    mapa_predipitacion_mitad_ano =filedialog.askopenfilename(filetypes=[("imagen del planeta",".png")])
    ruta_guardado = filedialog.asksaveasfilename(defaultextension=".png")
    print("empezando")
    imagen = skcc.koppen(mapa_temperatura,mapa_temperatura_mitad_ano,mapa_predipitacion,mapa_predipitacion_mitad_ano)
    

    imagen.save(ruta_guardado)
    print("terminado")

def Bioma_ventana_Emergente(ventana_principal):
    ventana_emergente = tk.Toplevel(ventana_principal)
    ventana_emergente.title(f"Biomas Koppen")

    bioma = tk.Button(ventana_emergente,text="biomas Koppen",command=Bioma)
    bioma.pack()

def main():
    # Crear una instancia de la clase Tk
    root = tk.Tk() # ventana principal
    root_ancho = 300 #root.winfo_screenwidth()
    root_alto = 100#root.winfo_screenheight()

    # Configurar la ventana principal
    root.title("Fantasy Map")
    ventxy = f"{root_ancho}x{root_alto}" 
    root.geometry(ventxy)  # Tamaño inicial de la ventana en píxeles (ancho x alto)
    marco_1 = tk.Frame(root)
    marco_1.pack(side=tk.TOP, padx=10, pady=10)


    button = tk.Button(marco_1,text="Mapa Altura",command=Sombra_lluvia)
    button.pack()

    bioma_ventana = tk.Button(marco_1,text="Bioma Koppen",command=Bioma)
    bioma_ventana.pack()
    

    # Ejecutar el bucle principal de Tkinter
    root.mainloop()

if __name__ == "__main__":
    ventana_principal()