import sys
import os
import importlib
import importlib.util

from PIL import Image, ImageEnhance, ImageOps,ImageDraw
from tqdm import tqdm
import numpy as np
import cv2
import random
import math

#import skcc

from calculadoras import skcc





class Mundo():
    def __init__(self,mapa_altura,mapa_temperatura,mapa_precipitacion):
        self.alt_map = Image.open(mapa_altura)
        self.temp_map = Image.open(mapa_temperatura)
        self.pre_map = Image.open(mapa_precipitacion)
        self.por_mon = 30
        self.por_mar = 7.5
    
    def poligonizar(self):
        alt_x,alt_y = self.alt_map.size
        div = 10
        for y in tqdm(range(alt_y),desc="calculando"):
            for x in range(alt_x):
                P_alt = self.alt_map.getpixel()
                V_alt = regla_de_tres(255,100,P_alt)
                if V_alt >= self.por_mon:
                    pass



#Funciones

def map_value_to_color(value, min_value, max_value):
    """esta funcion convierte valores numericos a valores rgb de 0 a 255"""
    normalized_value = (value - min_value) / (max_value - min_value)
    scaled_value = int(normalized_value * 255)
    color = (scaled_value, scaled_value, scaled_value)
    return color

def map_color_to_value(color, min_value, max_value):
    """esta funcion convierte valores rgb de 0 a 255 en valores numericos"""
    scaled_value = color  # Usamos el valor R de la escala de grises
    normalized_value = scaled_value / 255.0
    original_value = (normalized_value * (max_value - min_value)) + min_value
    return original_value

def Poligonizar(Imagen):
    imagen = Image.open(Imagen)
    ancho , alto = imagen.size
    subdiv = 10
    ancho2  = int(ancho/subdiv)
    alto2 = (alto/subdiv)
    for ya in tqdm(range(alto2),desc="busqueda de pixel"):
        for xa in range(ancho2):
            pass
    pass

def diametro_planeta(latitud_grados, radio_ecuatorial):
    # Convertir la latitud de grados a radianes
    latitud_radianes = math.radians(abs(latitud_grados))

    # Calcular el diámetro del planeta en el punto dado
    diametro = 2 * radio_ecuatorial * math.cos(latitud_radianes)

    return diametro

def calcular_latitus(pixel, alto_imagen):
    # Rango de píxeles para la transición (la mitad de la imagen)
    rango_transicion = alto_imagen // 2

    # Ángulo en grados para el píxel en la transición
    angulo_transicion = 90 * (rango_transicion - pixel) / rango_transicion

    # Si el píxel está en la segunda mitad de la imagen, invertir el ángulo
    if pixel >= rango_transicion:
        angulo_transicion = -angulo_transicion

    # Ángulo final según la transición
    angulo_final = abs(angulo_transicion)

    # Determinar si el píxel está en el hemisferio norte o sur
    direccion = "n" if pixel < rango_transicion else "s"

    return angulo_final, direccion

def vector_angu_magnitud(angle_degrees, magnitude):
    # Convertir el ángulo de grados a radianes
    angle_radians = math.radians(angle_degrees)

    # Calcular las componentes del vector
    x = magnitude * math.cos(angle_radians)
    y = magnitude * math.sin(angle_radians)

    return x, y

def  _Sombra_de_lluvia(Palt,altMax,diametro,ancho):
    """
    esta funcion calcula que tan grande es la sombra de lluvia
    Palt: es el valor del pixel de altitud de 0 a 255
    altMax: es la altura de la montañá mas alta del mundo (medido desde el fondo del mar) para darle al valor maximo de 255 de los pixeles
    diametro: el diametro del grado del planeta en donde estan
    ancho: es el ancho de la imagen
    """
    alt = regla_de_tres(altMax,255,Palt) # se calcula la altitud del pixel
    Som = 10 * alt # formula para calcular la sombra de lluvia
    Psombra = regla_de_tres(diametro,ancho,Som) # adaptar la distancia de la sombra con respecto al diametro del planeta en eslatitud
    return Psombra



def _latitudes(grado,ancho):
    if grado <= 90 and grado >= 60: # definir la direccion del viento
        return ancho
    elif grado <= 60 and grado >= 30: # definir la direccion del viento
        return 0
    elif grado <= 30 and grado >= 0: # definir la direccion del viento
        return ancho

regla_de_tres = lambda valor_conocido_deseado, valor_deseado, valor_conocido : (valor_conocido * valor_deseado) / valor_conocido_deseado



def angulo_flecha():
    def rotacion(ancho,alto,posicion):
        x,y = posicion

    ancho = 10000
    alto = 5000
    new = Image.new("RGBA",(ancho,alto),(0,0,0,0))
    flecha = Image.open("calculadoras\\flecha.png")
    fle_ancho = ancho//20
    fle_alto = alto//10
    flechaES = flecha.resize((fle_ancho,fle_alto)) # ajusta el tamaño de la flecha

    for x in range(20):
        for y in range(10):
            posicion = (x,y)
            xa = fle_ancho*x
            ya = fle_alto*y
            flecha_rotada = flechaES.rotate(rotacion(20,10,posicion))
            new.paste(flecha_rotada,(xa,ya),flecha_rotada)
    new.save("locuras.png")
    



def mapa_temperatura(mapa_altura,altura,OceanoPor):
    alt = Image.open(mapa_altura)
    ancho,alto = alt.size
    alto2 = alto /2
    new = Image.new("RGBA",(ancho,alto),(0,0,0,0))
    temp = [(187,65,168),(37,97,156),(120,211,235),(70,187,125),(22,114,57),(68,169,58),(233,241,114),(245,119,29),(239,56,30),(239,56,30),(245,119,29),(233,241,114),(68,169,58),(22,114,57),(70,187,125),(120,211,235),(37,97,156),(187,65,168)]
    templen = (len(temp))

    for x in range(ancho):
        for y in range(alto):
            if y <= alto2:
                a = int(regla_de_tres(alto,-templen,y))
                new.putpixel((x,y),temp[a])
            elif y >= alto2:
                a = int(regla_de_tres(alto,-templen,y))
                new.putpixel((x,y),temp[a])
    
    new.save("locuras.png")


def BiomaNoKoppen(MapaAlt,PorMon,PorMar,alt_max,MapTemp,MapPre,Nombre):
    TempMinMaxMedS = [(25,50,40),(20,45,35),(15,40,30),(10,35,25),(5,30,20),(0,25,15),(-10,20,5),(-20,10,-5),(-30,0,-15),(-40,-10,25)]
    TempSMax2 = max(TempMinMaxMedS)
    TempSMax = max(TempSMax2)
    TempSMin2 = min(TempMinMaxMedS)
    TempSMin = min(TempSMin2)

    
    mapaalt = Image.open(MapaAlt)
    mapatemp = Image.open(MapTemp)
    mapapre = Image.open(MapPre)
    ancho , alto = mapaalt.size
    new = Image.new("RGBA",(ancho,alto),(0,0,0,0))

    for y in range(alto):
        for x in range(ancho):
            x2 = 1800
            y2 = 1600
            alt = mapaalt.getpixel((x,y))
            #print(Pmaaalt,g,b,a)
            Tr2,Tg2,Tb2,a = mapatemp.getpixel((x,y))
            Tr = map_color_to_value(Tr2,TempSMin,TempSMax)
            Tg = map_color_to_value(Tg2,TempSMin,TempSMax)
            Tb = map_color_to_value(Tb2,TempSMin,TempSMax)
            pre = mapapre.getpixel((x,y))
            P = regla_de_tres(255,1500,pre[0])
            print(pre,P,Tb)
            altura = regla_de_tres(255,100,alt[0]) # da el porcentaje de la altura
            if altura > PorMar:
                if P < Tb:
                    new.putpixel((x,y),(254,0,0,255))
                else:
                    pass
    new.save(Nombre)


def Sombra_de_lluvia(img,alt_max,Alt_viento,equador_diam,Save):
    """
    esta funcion lo que hara es recorrer un mapa en blanco y negro creara otra imagen con las mismas dimenciones y transparente en donde en color blanco se marcara las llamadas sombra de lluvia
    img: la ruta del mapa de altura
    alt_max: al altura de la montaña mas alta del mundo (medido desde el fondo del mar) para darle al valor maximo de 255 de los pixeles
    Alt_viento: la altitud que se considera que una montaña interfiere con el viento para hacer una sombra de lluvia este tiene que ser de 0 a 100
    equador_diam: es el diametro del planeta en la linea del equador
    save: la ruta en la cuial se va a guardar el archivo
    """
    diam = equador_diam
    #diametro_planeta(0,diam)
    imgen = Image.open(img)
    ancho,alto = imgen.size
    Newimg = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))

    ps1 = 0 
    Ps = -1 
    PsA = 0 

    for y in range(alto):
        grado,ns = calcular_latitus(y,alto) # calcular la latitud
        diametro = diametro_planeta(grado,diam) # calcular el diametro en una latitud
        
        
        rev = _latitudes(grado,ancho)

        for x in range(ancho):
            x2 = abs(rev - x)
            color = imgen.getpixel((x2-1,y))
            r = color[0]
            altura = regla_de_tres(255,100,r) # da el porcentaje de la altura
            if altura >= Alt_viento:
                Ps = _Sombra_de_lluvia(r,alt_max,diametro,ancho)
                if altura < PsA:
                    ps1 = Ps
                PsA = altura
            elif altura <=50:
                Ps= 0
            
            if ps1 > 0:
                color = (255,255,255,255)
                Newimg.putpixel((x2-1,y),color)
                ps1 -= 1
            elif ps1 == 0:
                color = (0,0,0,0)
                Newimg.putpixel((x2-1,y),color)
            else:
                continue

            
            
            #
    
    #guardar imagen
    Newimg.save(Save)


def mapacolor(MapaAltura,Nombre):
    TempMinMaxMedN = [(-40,-10,-25),(-30,0,-15),(-20,10,-5),(-10,20,5),(0,25,15),(5,30,20),(10,35,25),(15,40,30),(20,45,35),(25,50,40)]
    TempMinMaxMedN.reverse()
    lenN = len(TempMinMaxMedN)
    TempNMAx2 = max(TempMinMaxMedN)
    TempNMAx = max(TempNMAx2)
    TempNMin2 = min(TempMinMaxMedN)
    TempNMin = min(TempNMin2)
    TempMinMaxMedS = [(25,50,40),(20,45,35),(15,40,30),(10,35,25),(5,30,20),(0,25,15),(-10,20,5),(-20,10,-5),(-30,0,-15),(-40,-10,25)]
    lenS = len(TempMinMaxMedS)
    TempSMax2 = max(TempMinMaxMedS)
    TempSMax = max(TempSMax2)
    TempSMin2 = min(TempMinMaxMedS)
    TempSMin = min(TempSMin2)
    mapaAltura = Image.open(MapaAltura)
    ancho,alto = mapaAltura.size
    new = Image.new("RGBA",(ancho,alto),(0,0,0,0))
    for y in range(alto):
        grado,ns = calcular_latitus(y,alto) # calcular la latitud
        
        for x in range(ancho):
            if ns == 'n':
                grad = int(regla_de_tres(90,lenN,grado)-1)
                Tmin = TempMinMaxMedN[grad][0]
                Tmax = TempMinMaxMedN[grad][1]
                Tmed = TempMinMaxMedN[grad][2]
                Pmin,r,g = map_value_to_color(Tmin,TempNMin,TempNMAx)
                Pmax,r,g = map_value_to_color(Tmax,TempNMin,TempNMAx)
                Pmed,r,g = map_value_to_color(Tmed,TempNMin,TempNMAx)
                new.putpixel((x,y),(Pmin,Pmax,Pmed))
                
            elif ns == 's':
                grad = int(regla_de_tres(90,lenN,grado)-1)
                Tmin = TempMinMaxMedS[grad][0]
                Tmax = TempMinMaxMedS[grad][1]
                Tmed = TempMinMaxMedS[grad][2]
                Pmin,r,g = map_value_to_color(Tmin,TempSMin,TempSMax)
                Pmax,r,g = map_value_to_color(Tmax,TempSMin,TempSMax)
                Pmed,r,g = map_value_to_color(Tmed,TempSMin,TempSMax)
                new.putpixel((x,y),(Pmin,Pmax,Pmed))
    new.save(Nombre)

# variables





radio_ecuatorial_tierra = 6371000.0
#alt_max = 21.287 # la altura maxima de mi mapa de altura que da como resultado a la montaña mas alta que es de 21.3 M
alt_max = 8.848
imagen = "Tierra.png"
imag2 = "terra3.png"

imagem = "Bump.bmp"
#imagen = "Tierra.png"
#save = "Sombra_de_lluvia.png"
#Alt_viento = 50
#Alt_viento = 25
#Sombra_de_lluvia(imagen,alt_max,Alt_viento,radio_ecuatorial_tierra,save)

#generate_temperature_map(imagen,imag2)

#Sombra_de_lluvia(imagem,alt_max,50,radio_ecuatorial_tierra,"sombralluvia.png")

#MapaHumedad(imagem,"sombralluvia.png",28.5,50,alt_max,"humee.png")
#MapaHumedad(imagen,imag2,7.5,9,alt_max,"Terrahumee.png")

#BiomaNoKoppen(imagen,30,7.5,alt_max,"TemperaturaTierra.png","Terrahumee.png","prueba.png")

#mapacolor(imagen,"TemperaturaTierra.png")



tempProfile,precProfile = skcc.defprofile()




tempFileNameNW1 ="ideas\speculative-koppen-master\\test\ProfiaTempJan.png"
tempFileNameNW2 = "Tierratemp.png"
tempFileNameNS1 ="ideas\speculative-koppen-master\\test\ProfiaTempJul.png"
precFileNameNW1 ="ideas\speculative-koppen-master\\test\ProfiaPrecJan.png"
precFileNameNW2 = "Tierraprec.png"
precFileNameNS1 ="ideas/speculative-koppen-master/test/ProfiaPrecJul.png"

outfileName = "terratrolas.png"

#imageng = skcc.koppen(tempFileNameNW2,tempFileNameNW2,precFileNameNW2,precFileNameNW2)



#print("terminamos")