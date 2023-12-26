"""
este modulo esta echo para ayudar a dibujar los layer de los niveles de sun de los mapas
"""


import os #la uso para crear carpetas
import sys

from PIL import Image # lo usamos para abrir guardar, modificar una imagen
import xml.etree.ElementTree as ET
from tkinter import filedialog

from rich.console import Console
from rich import print

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


    return (int(nivel-1),int(Carpeta-1),int(Imagen-1)),(pos_3,pos_4,pos_1,pos_2)

def crear_Carpetas(ruta) -> bool:
    if not os.path.exists(ruta):
        os.makedirs(ruta)
        return True
    else:
        return False

def tileLista(l:int,x0:int,y0:int,xF:int,yF:int)->list[list]:
    imagenesMax,carpetasMax = ima_carp_por_nivel(l)
    yDif = (yF-y0)+1
    xDif = (xF-x0)+1
    x02  = x0
    if xF<x0:
        xDif = (xDif-carpetasMax)%carpetasMax
        

    listaCarpetas = []
    listaImagenes = []
    temp = []

    for y in range(abs(yDif)):
        x0 =  x02
        listaCarpetas = []
        for x in range(abs(xDif)):
            if (x0+x) >= carpetasMax:
                pass
                #x0 = 0
            temp = (l,((x0+x)%carpetasMax),y0+y)
            listaCarpetas.append(temp)
        
        listaImagenes.append(listaCarpetas)
    
    return listaImagenes
    valorTemporal:bool = True # indicamos que es el primer valor porque el primer valor se recorre de manera distinta
    existentes:dict = {}
    for i2 in diccionario:
        listaTemp:list = []
        if valorTemporal == True:
            for i in diccionario[i2]:
                listaTemp2 = []
                for j in i:
                    ruta = path + f"\\{j[0]}\\{j[1]}\\{j[2]}"+formato
                    existe = os.path.exists(ruta)
                    listaTemp2.append(existe)
                valorTemporal = False
                listaTemp.append(listaTemp2)
        else:
            for i in diccionario[i2]:
                listaTemp2 = []
                for j in i:
                    rut = j[1][0]
                    ruta = path + f"\\{rut[0]}\\{rut[1]}\\{rut[2]}"+formato
                    existe = os.path.exists(ruta)
                    listaTemp2.append(existe)
                listaTemp.append(listaTemp2)
        existentes[i2] = listaTemp
        
    return existentes

def cortar_imagen(path,imagen,lista:list[bool,bool,bool,bool]):
    if imagen == False:
        img = Image.open(path)
    else:
        img = imagen
    ancho,alto = img.size
    ancho2 = ancho/2
    alto2 = alto/2
    cuadrantes = [(0,0,ancho2,alto2),(ancho2,0,ancho,alto2),(0,alto2,ancho2,alto),(ancho2,alto2,ancho,alto)]
    for i in range(4):
        if lista[i] == True:
            cortar = cuadrantes[i]
            break
        else:
            pass
    
    img2 = img.crop(cortar)
    ancho,alto = img2.size
    img3 = img2.resize((ancho*2,alto*2))
    return img3

def obtener_imagen(path,formato,hijo):
    padre, bol = padre_ref(hijo[0],hijo[1],hijo[2])
    ruta = path + f"\\{padre[0]}\\{padre[1]}\\{padre[2]}"+formato
    
    if os.path.exists(ruta):
        img2 = cortar_imagen(ruta,False,bol)
        return img2
    else:
        imgTemp = obtener_imagen(path,formato,padre)
        img3 = cortar_imagen(ruta,imgTemp,bol)
        return img3

def collage(path,formato,punto1,punto2,nivel,tamaño):
    listaHijos = tileLista(nivel,punto1[0],punto1[1],punto2[0],punto2[1])
    alto = (len(listaHijos))*tamaño
    ancho = (len(listaHijos[0]))*tamaño
    img = Image.new("RGB",(ancho,alto),(255,0,0))
    for numx,x in enumerate(listaHijos):
        for numy,y in enumerate(x):
            imgTemp = obtener_imagen(path,formato,y)
            img.paste(imgTemp,(tamaño*numy,tamaño*numx))
            #img.show()
    ruta = path + f"\\imagentemp3"+formato
    img.save(ruta)


ruta = "D:\\programa\\cesium\\Cesium-1.112\\Build\\CesiumUnminified\\Assets\\Textures\\Mundo"

formato = ".png"

punto1 = (30,8)
punto2 = (2,10)
nivel = 4
tamaño = 1024

#print(padre_ref(3,5,5))

collage(ruta,formato,punto1,punto2,nivel,tamaño)