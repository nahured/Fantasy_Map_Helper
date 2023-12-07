from PIL import Image, ImageEnhance, ImageOps,ImageDraw
from tkinter import filedialog
from tqdm import *


import math




# funciones

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

def  _sombra_de_lluvia(Palt,altMax,diametro,ancho):
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


def sombra_de_lluvia(img,alt_max,Alt_viento,equador_diam):
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
    newimg = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))

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
                Ps = _sombra_de_lluvia(r,alt_max,diametro,ancho)
                if altura < PsA:
                    ps1 = Ps
                PsA = altura
            elif altura <=50:
                Ps= 0
            
            if ps1 > 0:
                color = (255,255,255,255)
                newimg.putpixel((x2-1,y),color)
                ps1 -= 1
            elif ps1 == 0:
                color = (0,0,0,0)
                newimg.putpixel((x2-1,y),color)
            else:
                continue

    return newimg


def flujo_viento(link_imagen):
    imagen = Image.open(link_imagen)
    flecha_imagen = Image.open("calculadoras\\flecha.png")
    
    ancho,alto = imagen.size
    nueva_imagen = Image.new("RGBA",(ancho,alto),(0, 0, 0, 0))
    nuevo_tamano = (int(ancho/6),int(ancho/6))
    flecha_imagen = flecha_imagen.resize(nuevo_tamano)

    for x in range(nuevo_tamano[0]):
        print(f"\rProgreso: {x} de {nuevo_tamano[0]}", end="", flush=True)
        for y in range(nuevo_tamano[0]):
            nueva_imagen.paste(flecha_imagen,(0,0))
    
    nueva_imagen.show



def latitudes(lista_de_latitudes):# aca traza una linea en los limites de inclinacion del planeta con respecto a su sol
    imagen_file = filedialog.askopenfilename() # cargamos la ruta de la imagen
    save_iamgen = filedialog.asksaveasfilename(defaultextension=".png") # guardamos la ruta de la imagen
    imagen_pil = Image.open(imagen_file) # la importamos a pillow

    ancho,alto = imagen_pil.size  #optener el ancho y el alto de la iamgen

    new_imagen = Image.new("RGBA",(ancho,alto),(0,0,0,0)) # creamos una nueva imagen

    for x in range(ancho): # recorremos la imagen
        for y in range(alto):
            grado,ns = calcular_latitus(y,alto) # aca vemos en que latitud esta y

            if abs(grado) in lista_de_latitudes: # un if para verificar si y esta entre los grados 23 y 24
                new_imagen.putpixel((x,y),(255,0,0)) # aca pintamos ese pixel de rojo

    
    new_imagen.save(save_iamgen) # guardamos la imagen


def mapa_distancia_interna(diametro,mar,radio_interno):
    imagen_file = filedialog.askopenfilename() # cargamos la ruta de la imagen
    save_iamgen = filedialog.asksaveasfilename(defaultextension=".png") # guardamos la ruta de la imagen
    imagen_pil = Image.open(imagen_file) # la importamos a pillow

    ancho,alto = imagen_pil.size # optener el ancho y el alto de la iamgen

    new_imagen = Image.new("RGBA",(ancho,alto),(0,0,0,0)) # creamos una nueva imagen
    comienzo = [0,0]

    for y in range(alto):
        #print(f"\r {y}/{alto}",end="",flush=True)
        contador = 0
        lista_cruz = []
        grado,ns = calcular_latitus(y,alto) # calcular la latitud
        diametro_latitud = diametro_planeta(grado,diametro) # calcular el diametro en una latitud
        km_en_y = int(regla_de_tres(diametro_latitud,ancho,radio_interno))
        #print(km_en_y,"  ",ancho)
        #"""
        for x in range(ancho):
            alt_pixel_color = imagen_pil.getpixel((x,y))
            altura = regla_de_tres(255,100,alt_pixel_color[0]) # da el porcentaje de la altura
            if altura >= mar:
                if contador <= km_en_y:
                    new_imagen.putpixel((x,y),(0,255,0))
                contador += 1
                
            elif altura <= mar:
                contador = 0
        #"""
        
    new_imagen.save(save_iamgen)


def coordenadas_distancias(latitud1, latitud2, radio_tierra):
    # Conversión de grados decimales a radianes
    latitud1_rad = math.radians(latitud1)
    latitud2_rad = math.radians(latitud2)

    # Cálculo de la distancia aproximada usando la fórmula del semiverseno
    distancia = radio_tierra * math.acos(math.sin(latitud1_rad) * math.sin(latitud2_rad) + 
                                         math.cos(latitud1_rad) * math.cos(latitud2_rad))

    return distancia



Tamaño_de_píxel_x,Tamaño_de_píxel_y =	0.003741101310077289948,-0.003741101310077289948

Anchura =	7198
Altura = 	4228

print(Anchura*Tamaño_de_píxel_x)
print(Altura*Tamaño_de_píxel_y)