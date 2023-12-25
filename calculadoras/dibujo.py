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


def listaPadre(lista: list):
    temp = []
    elementos_encontrados = set()

    if type(lista[0][0]) == tuple and type(lista[0][0][0]) == int:
        for i in lista:
            temp2 = []
            for j in i:
                padre_ref_elemento = (j[0], j[1], j[2])
                if padre_ref_elemento not in elementos_encontrados:
                    padreRef = padre_ref(j[0], j[1], j[2])
                    temp2.append((j, padreRef))
                    elementos_encontrados.add(padre_ref_elemento)
            if len(temp2) >= 1: 
                temp.append(temp2)
    else:
        for i in lista:
            temp2 = []
            for j in i:
                cos = j[1][0]
                padre_ref_elemento = (cos[0], cos[1], cos[2])
                if padre_ref_elemento not in elementos_encontrados:
                    padreRef = padre_ref(cos[0], cos[1], cos[2])
                    temp2.append((j[1][0], padreRef))
                    elementos_encontrados.add(padre_ref_elemento)
            if len(temp2) >= 1: 
                temp.append(temp2)

    return temp


def tiles_totales(l:int,x0:int,y0:int,xF:int,yF:int):
    a =tileLista(l,x0,y0,xF,yF)
    tiles:dict = {}
    tiles[l] = a

    for i in range(l,0,-1):
        if a != False:
            f = listaPadre(a)
            tiles[f[0][1][1][0][0]] = f
            a = False
        else:
            f = listaPadre(f)
            tiles[f[0][1][1][0][0]] = f
    return tiles

def tiles_existentes(formato,path,diccionario:dict):
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
    if not imagen:
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

def opterne_imagenes(formato,path,diccionario:dict):
    imagenes:dict = {}
    clavesTotales = list(diccionario['total'])
    for i in clavesTotales:
        a = diccionario['total'][i]
        listaTemp = []
        for j in a:
            listaTemp2 = []
            for k in j:
                ruta = path + f"\\{k[0]}\\{k[1]}\\{k[2]}"+formato
                if not os.path.exists(ruta):
                    listaPath = []
                    ki = k
                    for i in range(ki[0],0,-1):
                        listaPath.append(k)
                        k,bol = padre_ref(k[0],k[1],k[2])
                        if os.path.exists(path + f"\\{k[0]}\\{k[1]}\\{k[2]}"+formato):
                            si = i
                            listaPath.append(k)
                            break
                    
                    primero = True
                    for i in listaPath.reverse():
                        if primero:
                            ruta = 
                            cortar_imagen()
                        pass


        

def armador(formato,path,l:int,x0:int,y0:int,xF:int,yF:int):
    imagenes:dict = {}
    imagenes["total"] = tiles_totales(l,x0,y0,xF,yF)
    imagenes["existentes"] = tiles_existentes(formato,path,imagenes["total"])
    imagenes["imagenes"] = opterne_imagenes(formato,path,imagenes)
    return imagenes

ruta = "D:\\programa\\cesium\\Cesium-1.112\\Build\\CesiumUnminified\\Assets\\Textures\\Mundo"

formato = ".png"
lel = armador(formato,ruta,3,4,0,2,3)

#consola.clear(True)
#print(lel)
