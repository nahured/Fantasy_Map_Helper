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


def listaPadre(lista:list):
    temp = []
    if type(lista[0][0]) == tuple and type(lista[0][0][0]) == int:
        for i in lista:
            temp2 = []
            for j in i:
                padreRef = padre_ref(j[0],j[1],j[2])
                temp2.append((j,padreRef))
            temp.append(temp2)
    else:
        for i in lista:
            temp2 = []
            for j in i:
                cos = j[1][0]
                padreRef = padre_ref(cos[0],cos[1],cos[2])
                temp2.append((j[1][0],padreRef))
            temp.append(temp2)
    

    return temp

def armardor(path,l:int,x0:int,y0:int,xF:int,yF:int):
    a =tileLista(l,x0,y0,xF,yF)
    imagenes:dict = {}
    imagenes[str(l)] = a

    for i in range(l,0,-1):
        if a != False:
            f = listaPadre(a)
            imagenes[f[0][1][1][0][0]] = f
            a = False
        else:
            f = listaPadre(f)
            imagenes[f[0][1][1][0][0]] = f

    
    return imagenes

ruta = "D:\\programa\\cesium\\Cesium-1.112\\Build\\CesiumUnminified\\Assets\\Textures\\Mundo"

lel = armardor(ruta,2,4,0,2,3)

for i in lel:
    print(i)
    print(f"-------\n{lel[i]}\n-------")

"""
a = tileLista(2,4,0,2,3)
f = listaPadre(a)
f2 = listaPadre(f)


print("----------")
for i in a:
    print(i)
print("----------")
for i in f:
    print(i)
print("----------")
for i in f2:
    print(i)
print("----------")
"""