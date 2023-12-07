"""
este modulo esta echo para ayudar a dibujar los layer de los niveles de sun de los mapas
"""


import os #la uso para crear carpetas
import sys

from PIL import Image # lo usamos para abrir guardar, modificar una imagen
import xml.etree.ElementTree as ET
from tkinter import filedialog

from rich.console import Console

consola = Console()

regla_de_tres = lambda a, b, c: (b * c) / a if a != 0 else None

def ima_carp_por_nivel(nivel)->int:
    """
    retorna la cantidad de carpetas e imagenes del nivel de zoom ingresado
    """

    imagenes = (2**nivel)
    carpetas = imagenes*2
    return (imagenes,carpetas)


def padre_ref(nivel,carpeta,imagen)->tuple[tuple[float,float,float],tuple[float,float,float]]:
    """
    encontrar cual es la imagen superior, y en que cuadrante de la imagen superior esta el nodo seleccionado
    """
    carpeta+=1
    imagen+=1
    nIma,nCarp = ima_carp_por_nivel(nivel)
    carpeta1 = regla_de_tres(nCarp,nIma,carpeta)
    imagen1 = regla_de_tres(nIma,nIma/2,imagen)
    Carpeta = -(-regla_de_tres(nCarp,nIma,carpeta)//1)
    Imagen = -(-regla_de_tres(nIma,nIma/2,imagen)//1)
    pos_1 = False if not((carpeta1-0.5)%1==0 and (imagen1-0.5)%1==0.5) else True
    pos_2 = False if not((carpeta1-0.5)%1==0.5 and (imagen1-0.5)%1==0.5) else True
    pos_3 = False if not((carpeta1-0.5)%1==0 and (imagen1-0.5)%1==0) else True
    pos_4 = False if not((carpeta1-0.5)%1==0.5 and (imagen1-0.5)%1==0) else True


    return (int(nivel-1),int(Carpeta-1),int(Imagen-1)),(pos_1,pos_2,pos_3,pos_4)


def dividir_imagen(img, num_filas, num_columnas):
    try:
        ancho, alto = img.size
        ancho_seccion = ancho // num_columnas
        alto_seccion = alto // num_filas

        secciones_dict = {}
        secciones_lista = []

        for i in range(num_filas):
            for j in range(num_columnas):
                izquierda = j * ancho_seccion
                arriba = i * alto_seccion
                derecha = (j + 1) * ancho_seccion
                abajo = (i + 1) * alto_seccion

                seccion = img.crop((izquierda, arriba, derecha, abajo))
                secciones_lista.append(seccion)

                # Generar un nombre único para cada sección
                nombre_seccion = f"seccion_{i}_{j}.png"
                secciones_dict[nombre_seccion] = seccion

        return secciones_dict, secciones_lista

    except Exception as e:
        print(f"Error al dividir la imagen: {e}")
        return None, None

def crear_Carpetas(ruta) -> bool:
    if not os.path.exists(ruta):
        os.makedirs(ruta)
        return True
    else:
        return False

class Proyecto:
    def __init__(self,ruta,tamaño,niveles):
        self.ruta = ruta
        self.tamaño = tamaño
        self.niveles = niveles

class Imagen:
    def __init__(self,ruta:str,tamaño:list[int],id:list[int],proyecto:Proyecto):
        self.ruta = ruta
        self.tamaño = tamaño
        self.id = id
        self.proyecto = proyecto
    
    def crear_Carpetas(ruta) -> bool:
        if not os.path.exists(ruta):
            os.makedirs(ruta)
            return True
        else:
            return False
    def dividir_imagen(img, num_filas, num_columnas):
        try:
            ancho, alto = img.size
            ancho_seccion = ancho // num_columnas
            alto_seccion = alto // num_filas

            secciones_dict = {}
            secciones_lista = []

            for i in range(num_filas):
                for j in range(num_columnas):
                    izquierda = j * ancho_seccion
                    arriba = i * alto_seccion
                    derecha = (j + 1) * ancho_seccion
                    abajo = (i + 1) * alto_seccion

                    seccion = img.crop((izquierda, arriba, derecha, abajo))
                    secciones_lista.append(seccion)

                    # Generar un nombre único para cada sección
                    nombre_seccion = f"seccion_{i}_{j}.png"
                    secciones_dict[nombre_seccion] = seccion

            return secciones_dict, secciones_lista

        except Exception as e:
            print(f"Error al dividir la imagen: {e}")
            return None, None

    def __ima_carp_por_nivel(nivel)->int:
        """
        retorna la cantidad de carpetas e imagenes del nivel de zoom ingresado
        """

        imagenes = (2**nivel)
        carpetas = imagenes*2
        return (imagenes,carpetas)


    def padre_ref(self,nivel,carpeta,imagen)->tuple[tuple[float,float,float],tuple[float,float,float]]:
        """
        encontrar cual es la imagen superior, y en que cuadrante de la imagen superior esta el nodo seleccionado
        """
        carpeta+=1
        imagen+=1
        nIma,nCarp = self.__ima_carp_por_nivel(nivel)
        carpeta1 = regla_de_tres(nCarp,nIma,carpeta)
        imagen1 = regla_de_tres(nIma,nIma/2,imagen)
        Carpeta = -(-regla_de_tres(nCarp,nIma,carpeta)//1)
        Imagen = -(-regla_de_tres(nIma,nIma/2,imagen)//1)
        return (nivel-1,Carpeta-1,Imagen-1),(nivel-1,carpeta1-0.5,imagen1-0.5)

    def guardar_mega_imagen(self):
        l,x,y = self.id

        pass

        
class Collage(Imagen):
    def __init__(self,ruta:str,imagenes:list[list:Imagen],nivel:int,rango:list[list[int,int],list[int,int]],limite:int):
        self.ruta = ruta
        self.imagenes = imagenes
        self.rango = rango #[[],[]]
        self.nivel = nivel
        self.limite = limite # el limite de pixeles que tiene que tener una imagen
    
    def crear_collage(self):
        imagenes,carpetas = self.__ima_carp_por_nivel(self.nivel)
        esquinaA:list[int,int] = self.rango[0]
        esquinaB:list[int,int] = self.rango[1]
        ancho = (esquinaB[0] - esquinaA[0])+1 if esquinaB[0] >= esquinaA[0] else (esquinaB[0] - (esquinaA[0]-carpetas))+1
        alto =  (esquinaA[1] - esquinaB[1])+1 if esquinaB[1] <= esquinaA[1] else (esquinaB[1] - (esquinaA[1]-imagenes))+1
        imh = 1000/(2*2*2)
        print((ancho+1)*imh,(alto+1)*imh,imh)
        print(f"ancho {ancho} ,alto {alto},{ancho*1000} {alto*1000} ,imagenes {imagenes} ,carpetas {carpetas}")
    
    def crear_Carpetas(ruta) -> bool:
        if not os.path.exists(ruta):
            os.makedirs(ruta)
            return True
        else:
            return False
    
    def imagenes_existentes(self,padres_imagenes:dict) -> list:
        imagen_no_existente = {}
        imagen_existente = {}
        for dic in padres_imagenes:
            ruta_archivo = self.ruta + "\\" + str(padres_imagenes[dic][0][0]) + "\\"  + str(padres_imagenes[dic][0][1]) + "\\" + str(padres_imagenes[dic][0][2]) + ".png"
            if os.path.exists(ruta_archivo):
                imagen_existente[dic] = padres_imagenes[dic][0]
            else:
                l,x,y = padres_imagenes[dic][0]
                padre_a,pos = padre_ref(l,x,y)
                if str(padre_a) in imagen_no_existente:
                    imagen_no_existente[str(padre_a)] = [padre_a,[pos[0] if (imagen_no_existente[str(padre_a)][1][0] != True) else imagen_no_existente[str(padre_a)][1][0],pos[1] if (imagen_no_existente[str(padre_a)][1][1] != True) else imagen_no_existente[str(padre_a)][1],pos[2] if (imagen_no_existente[str(padre_a)][1][2] != True) else imagen_no_existente[str(padre_a)][1][2],pos[3] if (imagen_no_existente[str(padre_a)][1][3] != True) else imagen_no_existente[str(padre_a)][1][3]]]
                    pass
                else:
                    imagen_no_existente[str(padre_a)] = [[l,x,y],pos]
        return imagen_no_existente,imagen_existente
        
    def crear_collage(self,punta_a:list[int,int,int],punta_b:list[int,int,int]):
        limite_x = True if ((punta_a[1] - punta_b[1]) >= self.limite) else False
        limite_y = True if ((punta_a[2] - punta_b[2]) >= self.limite) else False
        if not limite_x and not limite_y:
            puntos_X = (punta_a[1] - punta_b[1])
            puntos_Y = (punta_a[2] - punta_b[2])
            #punta_a[1] = punta_a[1] - puntos_X
            #punta_a[2] = punta_a[2] - puntos_Y
            lista = []
            padres_imagenes = {}
            padres_imagenes_ref = {}
            for y in range(abs(puntos_Y)+1):
                mini_lista = []
                for x in range(abs(puntos_X)+1):
                    mini_lista.append([punta_a[0],punta_a[1]+x,punta_a[2]-y])
                    padre_a,pos = padre_ref(punto_a[0],punta_a[1]+x,punta_a[2]-y)
                    if str(padre_a) in padres_imagenes:
                        padres_imagenes[str(padre_a)] = [padres_imagenes[str(padre_a)][0],[pos[0] if (padres_imagenes[str(padre_a)][1][0] != True) else padres_imagenes[str(padre_a)][1][0],pos[1] if (padres_imagenes[str(padre_a)][1][1] != True) else padres_imagenes[str(padre_a)][1][1],pos[2] if (padres_imagenes[str(padre_a)][1][2] != True) else padres_imagenes[str(padre_a)][1][2],pos[3] if (padres_imagenes[str(padre_a)][1][3] != True) else padres_imagenes[str(padre_a)][1][3]]]
                    else:
                        padres_imagenes_ref[str(padre_a)]=padre_a
                        padres_imagenes[str(padre_a)] = [padre_a,[pos[0],pos[1],pos[2],pos[3]]]
                lista.append(mini_lista)           
            

            imagen_no_existente,imagen_existente = self.imagenes_existentes(padres_imagenes)
            imagen_no_existente,imagen_existenteA = self.imagenes_existentes(imagen_no_existente)
            imagen_existente.update(imagen_existenteA)
            imagen_no_existente,imagen_existenteA = self.imagenes_existentes(imagen_no_existente)
            imagen_existente.update(imagen_existenteA)
            print(imagen_no_existente,"\n\n",imagen_existente,"\n---------\n")
            return lista,padres_imagenes,padres_imagenes_ref


        else:
            print(f"limite_x {limite_x} > {self.limite} \n limite_y {limite_y} > {self.limite}")
    
    def guardar_mega_collage(self):
        imagenes,carpetas = ima_carp_por_nivel(self.nivel)
        img = self.imagenes
        diccionario_secciones, lista_secciones = dividir_imagen(img,imagenes,carpetas)
        nombre = imagenes-1
        nombre_carpeta = 0
        if diccionario_secciones is not None:
            # Guardar las imágenes fuera de la función
            for nom, seccion in diccionario_secciones.items():
                ruta_completa = self.ruta + "\\" +str(nombre_carpeta) +"\\"+ str(nombre) + ".png"
                seccion.save(ruta_completa)
                if nombre_carpeta < (carpetas-1):
                    nombre_carpeta += 1 
                else:
                    nombre_carpeta = 0
                    nombre -= 1

        



#sys.exit()
proyecto_ruta = "E:\\programas\\cesium\\Cesium-1.111\\Build\\CesiumUnminified\\Assets\\Textures\\Mundo"
ruta3 = "F:\\obsidian\\ProyectoReinado\\Recursos\\imagenes\\mapa\\WILBUR\\Mundo\\diviciones\\xport2\\1"

imagen1 = Collage(
    proyecto_ruta,
    Image.open("E:\\programas\\cesium\\Cesium-1.111\\Build\\CesiumUnminified\\Assets\\Textures\\Mundo\\2\\2\\1.png"),
    2,
    3,
    1000
    )


punto_a = [5,17,12]
punto_b = [5,21,10]


lista, padre_dic,padres_imagenes_ref = imagen1.crear_collage(punto_a,punto_b)

for dic in padre_dic:
    print(padres_imagenes_ref[dic])



