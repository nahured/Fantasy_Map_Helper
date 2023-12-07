#! /usr/bin/python
# -*- coding: utf-8 -*-

# Speculative Köppen-Geiger Climate Classifier
# (c) 2018-2020 Patrick Harvey (see LICENSE.txt)

import sys, getopt, itertools, re, time
from PIL import Image
from calculadoras.utils.errors import *
#from utils.errors import SKCCError
from calculadoras.ioHandling.inputHandler import readInputProfile, InputProfile
from calculadoras.ioHandling.outputHandler import readOutputProfile, OutputProfile

import math





versionNumber = '0.0.8'

modes = {'koppen', 'holdridge'}

kColorTableDefault = {'Af':(11, 36, 250), 'As':(76, 171, 247), 'Aw':(76, 171, 247), 'Am':(21, 123, 251), 
               'Cfa':(199, 253, 92), 'Csa':(255, 253, 56), 'Cwa':(153, 253, 154),
               'Cfb':(109, 253, 70), 'Csb':(198, 197, 41), 'Cwb':(103, 197, 104),
               'Cfc':(60, 197, 35), 'Csc':(198, 197, 41), 'Cwc':(103, 197, 104),
               'Dfa':(45, 255, 254), 'Dsa':(252, 40, 251), 'Dwa':(172, 179, 253),
               'Dfb':(66, 200, 252), 'Dsb':(196, 29, 197), 'Dwb':(92, 122, 216),
               'Dfc':(16, 126, 124), 'Dsc':(149, 55, 147), 'Dwc':(77, 84, 178),
               'Dfd':(6, 69, 93), 'Dsd':(149, 101, 148), 'Dwd':(50, 14, 133),
               'ET':(178, 178, 178), 'EF':(104, 104, 104),
               'BSh':(243, 162, 39), 'BSk':(254, 218, 108), 'BWh':(251, 13, 27), 'BWk':(252, 151, 151)}

hColorTableDefault = {'Ice':(255, 255, 255), 'Polar desert':(214, 214, 214), 
                      'Subpolar dry tundra':(111, 131, 132), 'Subpolar moist tundra':(111, 131, 132),
                      'Subpolar wet tundra':(111, 131, 132), 'Subpolar rain tundra':(111, 131, 132), 
                      'Boreal desert':(222, 207, 143), 'Boreal dry scrub':(181, 180, 130),
                      'Boreal moist forest':(34, 96, 96), 'Boreal wet forest':(34, 96, 96), 
                      'Boreal rain forest':(34, 96, 96), 'Cool temperate desert':(222, 207, 143),
                      'Cool temperate desert scrub':(181, 180, 130), 'Cool temperate steppe':(85, 153, 84),
                      'Cool temperate moist forest':(27, 153, 119), 'Cool temperate wet forest':(27, 153, 119),
                      'Cool temperate rain forest':(27, 153, 119), 'Warm temperate desert':(254, 224, 92), 
                      'Warm temperate desert scrub':(194, 195, 101), 'Warm temperate thorn scrub':(132, 202, 90),
                      'Warm temperate dry forest':(132, 202, 90), 'Warm temperate moist forest':(32, 203, 126), 
                      'Warm temperate wet forest':(32, 203, 126), 'Warm temperate rain forest':(32, 203, 126),
                      'Subtropical desert':(254, 224, 92), 'Subtropical desert scrub':(194, 195, 101), 
                      'Subtropical thorn woodland':(202, 232, 94), 'Subtropical dry forest':(94, 230, 95),
                      'Subtropical moist forest':(94, 230, 95), 'Subtropical wet forest':(41, 177, 72), 
                      'Subtropical rain forest':(41, 177, 72), 'Tropical desert':(254, 224, 92),
                      'Tropical desert scrub':(194, 195, 101), 'Tropical thorn woodland':(202, 232, 94), 
                      'Tropical very dry forest':(202, 232, 94), 'Tropical dry forest':(94, 230, 95),
                      'Tropical moist forest':(41, 177, 72), 'Tropical wet forest':(41, 177, 72), 
                      'Tropical rain forest':(41, 177, 72)}

tColorTableDefault = {(160, 0, 65):38, (210, 60, 80):31, (245, 110, 65):25, (250, 175, 95):20,
               (255, 225, 140):14, (230, 245, 150):5, (170, 220, 165):-5, (100, 195, 165):-18,
               (50, 135, 190):-32, (95, 80, 160):-40}



pColorTableDefault = {(135, 0, 180):300.0, (130, 60, 200):170.0, (105, 70, 200):105.0, (60, 60, 180):55.0, 
               (70, 95, 150):30.0, (55, 85, 100):15.0, (35, 50, 50):7.5, (20, 20, 20):2.5}

defaultOceanColor = (107, 165, 210)

defaultUnknownColor = (0, 0, 0)


# Función para calcular la distancia de color entre dos tuplas RGB
def distancia_color(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

# Función para reemplazar los colores de una imagen con los colores más cercanos en una lista
def verificar_color2(modo,imagen_path):
    # Define las listas de colores
    tColor = ((160, 0, 65),(210, 60, 80),(245, 110, 65),(250, 175, 95),(255, 225, 140),(230, 245, 150),(170, 220, 165),(100, 195, 165),(50, 135, 190),(95, 80, 160),(107,165,210))
    pColor = ((107, 165, 210), (135, 0, 180), (130, 60, 200), (105, 70, 200), (60, 60, 180),
              (70, 95, 150), (55, 85, 100), (35, 50, 50), (20, 20, 20))

    # Selecciona la lista de colores según el modo
    if modo == 't':
        lista_rgb = tColor
    elif modo == 'p':
        lista_rgb = pColor
    else:
        raise ValueError("Modo no válido. Use 't' para tColor o 'p' para pColor.")

    # Abre la imagen
    imagen = Image.open(imagen_path)
    ancho,alto =imagen.size

    # Crea una nueva imagen para almacenar el resultado
    nueva_imagen = Image.new("RGB", imagen.size)
    n = 0

    # Itera sobre los píxeles de la imagen
    for x in range(ancho):
        n += 1
        for y in range(alto):

            if n >=1000:
                n = 0
                print(f"\r x={x} {ancho-x}|y = {y}",end="",flush=True)
            pixel = imagen.getpixel((x, y))
            if pixel not in lista_rgb:

                # Encuentra el color más cercano en la lista_rgb
                color_mas_cercano = min(lista_rgb, key=lambda color: distancia_color(pixel, color))

                # Asigna el color más cercano al nuevo píxel
                nueva_imagen.putpixel((x, y), color_mas_cercano)

    # Retorna la nueva imagen
    return nueva_imagen


def verificar_color(tipo,imagen):
    tipos = "tp"
    tColor = ((160, 0, 65),(210, 60, 80),(245, 110, 65),(250, 175, 95),(255, 225, 140),(230, 245, 150),(170, 220, 165),(100, 195, 165),(50, 135, 190),(95, 80, 160),(107,165,210))
    pColor = ((107,165,210),(135, 0, 180),(130, 60, 200),(105, 70, 200),(60, 60, 180),(70, 95, 150),(55, 85, 100),(35, 50, 50),(20, 20, 20))

    if tipo in tipos:
        imag = Image.open(imagen)
        im_x = imag.width
        im_y = imag.height

        if tipo == "t":
            for x in range(im_x):
                for y in range(im_y):
                    pixel = imag.getpixel((x,y))
                    if pixel in tColor:
                        pass
                    else:
                        return ((x,y),pixel)
        elif tipo == "p":
            for x in range(im_x):
                for y in range(im_y):
                    pixel = imag.getpixel((x,y))
                    if pixel in pColor:
                        pass
                    else:
                        return ((x,y),pixel)




# Configurar perfiles de color por defecto
def defprofile():
    tempProfile = InputProfile(tColorTableDefault, [defaultOceanColor])
    precProfile = InputProfile(pColorTableDefault, [defaultOceanColor])
    return tempProfile,precProfile

def usage():
    print('''skcc.py : Clasificador Especulativo de Climas Köppen-Geiger
  Convierte los datos de temperatura y precipitación de entrada en un mapa pintado con
  las categorías de clima Köppen-Geiger correspondientes.
  Opciones:
    -h, --ayuda    : Muestra este mensaje
    -v, --version  : Muestra la versión actual de skcc.py
    -s, --silencio : Silencia la salida de finalización exitosa
    -d, --depurar  : Muestra trazas de pila para errores en tiempo de ejecución (por defecto, desactivado)
    -m, --modo     : Establece el modo operativo (qué clasificar). Por defecto, el modo Köppen si no se proporciona. Las configuraciones válidas son
                     'koppen' u 'holdridge'.
    -o<fname>, --archivo_salida=<fname>  : Guarda la imagen resultante en la ruta de archivo '<fname>',
                                           requiere dos entradas de temperatura y dos de precipitación. Requerido.
    -t<fname>, --tempnw=<fname>   : Toma los datos de temperatura para el invierno del hemisferio norte
                                    de la imagen '<fname>'. Requerido.
    -u<fname>, --tempns=<fname>   : Toma los datos de temperatura para el verano del hemisferio norte
                                    de la imagen '<fname>'. Requerido.
    -p<fname>, --precnw=<fname>   : Toma los datos de precipitación para el invierno del hemisferio norte
                                    de la imagen '<fname>'. Requerido.
    -q<fname>, --precns=<fname>   : Toma los datos de precipitación para el verano del hemisferio norte
                                    de la imagen '<fname>'. Requerido.
    -v<fname>, --perfiltemp=<fname> : Toma el perfil de color de temperatura de entrada del archivo '<fname>'.
    -r<fname>, --perfilprec=<fname> : Toma el perfil de color de precipitación de entrada del archivo '<fname>'.
    -k<fname>, --perfilsalida=<fname> : Toma el perfil de color de salida del archivo '<fname>'. ''')
    sys.exit(0)

def version():
    print('''skcc.py: v''' + versionNumber)
    sys.exit(0)

def optErr():
    raise SKCCError('Invalid options. Use the \'-h\' or \'--help\' options for usage information.')

def outputToFile(filename, img):
    try:
        img.save(filename)
    except:
        raise SKCCError('Could not write to file' + filename)

# Converts an input pixel color to a temperature value.
def getTemperatureCategory(tPixel, tempProfile):
    return tempProfile.getValue(tPixel)

# Converts an input pixel color to a precipitation value.
def getPrecipCategory(pPixel, precProfile):
    return precProfile.getValue(pPixel)

# Returns (summer temp, winter temp), (summer precip category, winter precip category)
# tuples from raw pixel data 
def convertPixelData(pxTuple, tempProfile, precProfile, isNorthernHemis):
    if isNorthernHemis:
        return ((getTemperatureCategory(pxTuple[0], tempProfile), getTemperatureCategory(pxTuple[1], tempProfile)), 
                (getPrecipCategory(pxTuple[2], precProfile), getPrecipCategory(pxTuple[3], precProfile)))
    else:
        return ((getTemperatureCategory(pxTuple[1], tempProfile), getTemperatureCategory(pxTuple[0], tempProfile)),
                (getPrecipCategory(pxTuple[3], precProfile), getPrecipCategory(pxTuple[2], precProfile)))

# Returns True iff any color in the pixel is ignored for the input profiles.
def pixelTupleIsIgnored(pxTuple, tempProf, precProf):
    return any(tempProf.isIgnored(px) for px in pxTuple[0:2]) or any(precProf.isIgnored(px) for px in pxTuple[2:4])

# Returns the climate letter (first part) of the climate classification
# based on the temperature and assuming it is not arid
def getTemperatureType(tempTuple):
    maxTemp = max(tempTuple[0], tempTuple[1])
    minTemp = min(tempTuple[0], tempTuple[1])
    if (minTemp > 18):
        #If cold month has above 18 degrees C
        return 'A'
    elif (maxTemp < 10):
        #If hot month has below 10 degrees C
        return 'E'
    elif (minTemp >= 0):
        #If cold month has above 0 degrees C
        return 'C'
    else:
        return 'D'

# Returns (evaporation estimate R, annual precipitation estimate)
# The aridity threshold formulae are adapted from 'World Map of the Köppen-Geiger 
# climate classification updated', Kottek et al. 2006.
def getEvaEstimate(tempTuple, precTuple):
    tAnn = (tempTuple[0] + tempTuple[1]) / 2.0
    summerPrecip = precTuple[0]
    winterPrecip = precTuple[1]
    summerEst = summerPrecip * 6.0
    winterEst = winterPrecip * 6.0
    annualEst = summerEst + winterEst
    summerPrecipPercent = (summerEst / annualEst) * 100.0
    if (summerPrecipPercent > 66.667):
        return (10.0 * ((2.0 * tAnn) + 28.0), annualEst)
    elif (summerPrecipPercent < 33.333):
        return (10.0 * (2.0 * tAnn), annualEst)
    else:
        return (10.0 * ((2.0 * tAnn) + 14.0), annualEst)

# Returns the precipitation pattern for a pixel's climate class
# for non-arid climates.
def getPrecipitationPattern(tType, tempTuple, precTuple, annualPrecip):
    if (tType == 'A'):
        if ((precTuple[0] > 60) and (precTuple[1] > 60)):
            return 'f'
        else:
            wThresh = 100 - (annualPrecip / 25.0)
            dryPrecip = min(precTuple[0], precTuple[1])
            if (dryPrecip >= wThresh):
                return 'm'
            elif (precTuple[1] < 60):
                return 'w'
            else:
                return 's'
    elif ((tType == 'C') or (tType == 'D')):
        if (precTuple[1] < (precTuple[0] * 0.1)):
            return 'w'
        elif ((precTuple[0] < (precTuple[1] * 0.33)) and (precTuple[0] < 40)):
            return 's'
        else:
            return 'f'
    elif (tType == 'E'):
        if (max(tempTuple[0], tempTuple[1]) < 0):
            return 'F'
        else:
            return 'T'
    else:
        raise SKCCError('Invalid climate category for getPrecipitationPattern; should never happen')

# Gets the seasonal pattern (third letter) for non-A/E climates.
# A or E climates simply return 'x' which is used as a placeholder marker value
def getSeasonalPattern(tType, tempTuple):
    if (tType == 'B'):
            avgTemp = (tempTuple[0] + tempTuple[1]) / 2.0
            if (avgTemp >= 18.0):
                return 'h'
            else:
                return 'k'
    elif (tType == 'C'):
            if (tempTuple[0] >= 22):
                return 'a'
            elif ((tempTuple[1] < 10) and (tempTuple[0] < 13)):
                return 'c'
            else:
                return 'b'
    elif (tType == 'D'):
            if (tempTuple[0] >= 22):
                return 'a'
            elif (tempTuple[1] < -38):
                return 'd'
            elif ((tempTuple[1] < -10) and (tempTuple[0] <= 14)):
                return 'c'
            else:
                return 'b'
    else:
        return 'x'

# Given an input pixel from each input map, returns an output color value
# corresponding to its climate class according to the output profile's color mapping.
def getClimateColor(pxTuple, tempProfile, precProfile, outProfile, isNorthernHemis):
    # pxTuple contains a tuple of four pixels, for (temp1, temp2, precip1, precip2).
    # If this pixel in any input has the ocean color we treat this pixel as ocean and ignore it.
    if pixelTupleIsIgnored(pxTuple, tempProfile, precProfile):
        return outProfile.ignoredColor
    else:
        tempTuple, precTuple = convertPixelData(pxTuple, tempProfile, precProfile, isNorthernHemis)
        #Temptuple is (avg. for summer, avg. for winter)
        #precTuple is (category for summer, category for winter)
        tType = getTemperatureType(tempTuple)
        pType = 'f' #Placeholder value

        annualPrecip = 0.0 # Placeholder value
        #Check for aridity (polar climate category exempted)
        if (tType != 'E'):
            evaporation, annualPrecip = getEvaEstimate(tempTuple, precTuple)
            if (annualPrecip < (evaporation / 2.0)):
                tType = 'B'
                pType = 'W'
            elif (annualPrecip < evaporation):
                tType = 'B'
                pType = 'S'

        if (tType != 'B'):
            pType = getPrecipitationPattern(tType, tempTuple, precTuple, annualPrecip)
        
        stType = getSeasonalPattern(tType, tempTuple)

        climateCode = tType + pType
        if (stType != 'x'):
            climateCode = climateCode + stType
        if (climateCode in outProfile.colorTable):
            return outProfile.colorTable[climateCode]
        else:
            raise SKCCError('Invalid Köppen-Geiger climate class (should never happen): ' + climateCode)


# Bounds a temperature to make a biotemperature, to 30 degrees C ceiling or 0 degrees C floor.
def boundTemperature(temp):
    return min(max(temp, 0), 30)

# Given a tuple of temperatures (extreme 1, extreme 2), compute an average biotemperature extrapolation.
# Uses a sine-wave approximation to interpolate between month temperatures, then applies
# 30 degrees C or 0 degrees C as a ceiling and floor respectively, then sums up and averages over all 12 months.
def getBiotemperature(tempTuple):
    tempTotal = 0
    tempTotal += boundTemperature(tempTuple[0])
    # Coefficients precomputed and hardcoded for speed
    # Are (sin(pi/6)+1)/2, 1-(sin(pi/6)+1)/2), (sin(pi/3)+1)/2, etc.
    tempTotal += 2*boundTemperature((tempTuple[0]*0.9330127)+(tempTuple[1]*0.0669873))
    tempTotal += 2*boundTemperature((tempTuple[0]*0.75)+(tempTuple[1]*0.25))
    tempTotal += 2*boundTemperature((tempTuple[0]*0.5)+(tempTuple[1]*0.5))
    tempTotal += 2*boundTemperature((tempTuple[0]*0.25)+(tempTuple[1]*0.75))
    tempTotal += 2*boundTemperature((tempTuple[0]*0.0669873)+(tempTuple[1]*0.9330127))
    tempTotal += boundTemperature(tempTuple[1])
    return tempTotal / 12

# Looks up a life zone category and gets the color given a biotemperature and
# annual precipitation estimate.
# 17 degrees C is used as the 'critical temperature line' delineating the
# definition of subtropical vs. warm temperate.
def lookupLifeZoneColor(bioTemp, precTotal, outProfile):
    if (bioTemp <= 0):
        return outProfile.colorTable['Ice']
    elif (bioTemp < 1.5):
        return outProfile.colorTable['Polar desert']
    elif (bioTemp < 3):
        if (precTotal < 125):
            return outProfile.colorTable['Subpolar dry tundra']
        elif (precTotal < 250):
            return outProfile.colorTable['Subpolar moist tundra']
        elif (precTotal < 500):
            return outProfile.colorTable['Subpolar wet tundra']
        else:
            return outProfile.colorTable['Subpolar rain tundra']
    elif (bioTemp < 6):
        if (precTotal < 125):
            return outProfile.colorTable['Boreal desert']
        elif (precTotal < 250):
            return outProfile.colorTable['Boreal dry scrub']
        elif (precTotal < 500):
            return outProfile.colorTable['Boreal moist forest']
        elif (precTotal < 1000):
            return outProfile.colorTable['Boreal wet forest']
        else:
            return outProfile.colorTable['Boreal rain forest']
    elif (bioTemp < 12):
        if (precTotal < 125):
            return outProfile.colorTable['Cool temperate desert']
        elif (precTotal < 250):
            return outProfile.colorTable['Cool temperate desert scrub']
        elif (precTotal < 500):
            return outProfile.colorTable['Cool temperate steppe']
        elif (precTotal < 1000):
            return outProfile.colorTable['Cool temperate moist forest']
        elif (precTotal < 2000):
            return outProfile.colorTable['Cool temperate wet forest']
        else:
            return outProfile.colorTable['Cool temperate rain forest']
    elif (bioTemp < 17):
        if (precTotal < 125):
            return outProfile.colorTable['Warm temperate desert']
        elif (precTotal < 250):
            return outProfile.colorTable['Warm temperate desert scrub']
        elif (precTotal < 500):
            return outProfile.colorTable['Warm temperate thorn scrub']
        elif (precTotal < 1000):
            return outProfile.colorTable['Warm temperate dry forest']
        elif (precTotal < 2000):
            return outProfile.colorTable['Warm temperate moist forest']
        elif (precTotal < 4000):
            return outProfile.colorTable['Warm temperate wet forest']
        else:
            return outProfile.colorTable['Warm temperate rain forest']
    elif (bioTemp < 24):
        if (precTotal < 125):
            return outProfile.colorTable['Subtropical desert']
        elif (precTotal < 250):
            return outProfile.colorTable['Subtropical desert scrub']
        elif (precTotal < 500):
            return outProfile.colorTable['Subtropical thorn woodland']
        elif (precTotal < 1000):
            return outProfile.colorTable['Subtropical dry forest']
        elif (precTotal < 2000):
            return outProfile.colorTable['Subtropical moist forest']
        elif (precTotal < 4000):
            return outProfile.colorTable['Subtropical wet forest']
        else:
            return outProfile.colorTable['Subtropical rain forest']
    else:
        if (precTotal < 125):
            return outProfile.colorTable['Tropical desert']
        elif (precTotal < 250):
            return outProfile.colorTable['Tropical desert scrub']
        elif (precTotal < 500):
            return outProfile.colorTable['Tropical thorn woodland']
        elif (precTotal < 1000):
            return outProfile.colorTable['Tropical very dry forest']
        elif (precTotal < 2000):
            return outProfile.colorTable['Tropical dry forest']
        elif (precTotal < 4000):
            return outProfile.colorTable['Tropical moist forest']
        elif (precTotal < 8000):
            return outProfile.colorTable['Tropical wet forest']
        else:
            return outProfile.colorTable['Tropical rain forest']

# Given an input pixel from each input map, returns an output color value
# corresponding to its Holdridge life zone category according to the output profile's color mapping.
def getLifeZoneColor(pxTuple, tempProfile, precProfile, outProfile):
    if pixelTupleIsIgnored(pxTuple, tempProfile, precProfile):
        return outProfile.ignoredColor
    else:
        tempTuple = (getTemperatureCategory(pxTuple[0], tempProfile), getTemperatureCategory(pxTuple[1], tempProfile))
        precTuple = (getPrecipCategory(pxTuple[2], precProfile), getPrecipCategory(pxTuple[3], precProfile))
        biotemp = getBiotemperature(tempTuple)
        precTotal = ((precTuple[0]*6)+(precTuple[1]*6))
        return lookupLifeZoneColor(biotemp, precTotal, outProfile)

# Returns a function to retrieve the RGB color values of a pixel.
def makeRGBConversion(img1, img2, img3, img4):
    bands = [img1.getbands(), img2.getbands(), img3.getbands(), img4.getbands()]
    bandIds = []
    for bandList in bands:
        if not ('R' in bandList):
            raise SKCCError('No red color channel in one or more input images.')
        elif not ('G' in bandList):
            raise SKCCError('No green color channel in one or more input images.')
        elif not ('B' in bandList):
            raise SKCCError('No blue color channel in one or more input images.')
        else:
            bandIds.append((bandList.index('R'), bandList.index('G'), bandList.index('B')))
    if (bandList[0] == ('R', 'G', 'B')) and (bandList[1] == ('R', 'G', 'B')) and (bandList[2] == ('R', 'G', 'B')) and (bandList[3] == ('R', 'G', 'B')):
        # Special case to improve performance if input is all RGB images with no channels
        def retRGB(pxTuple):
            return pxTuple
        return retRGB
    else:
        def getRGB(pxTuple):
            return ((pxTuple[0][bandIds[0][0]], pxTuple[0][bandIds[0][1]], pxTuple[0][bandIds[0][2]]),
                    (pxTuple[1][bandIds[1][0]], pxTuple[1][bandIds[1][1]], pxTuple[1][bandIds[1][2]]),
                    (pxTuple[2][bandIds[2][0]], pxTuple[2][bandIds[2][1]], pxTuple[2][bandIds[2][2]]),
                    (pxTuple[3][bandIds[3][0]], pxTuple[3][bandIds[3][1]], pxTuple[3][bandIds[3][2]]))
        return getRGB
    

# Construye una imagen en bruto que representa la clasificación correspondiente al modo seleccionado
# basándose en los mapas de temperatura y precipitación de entrada, interpretados a través de los perfiles de color
# de temperatura y precipitación de entrada.
def buildOutput(t1name, t2name, p1name, p2name, tempProfile, precProfile, outProfile, mode='koppen'):
    temperature1 =  Image.open(t1name)
    temperature2 =  Image.open(t2name)
    precipitation1 =  Image.open(p1name)
    precipitation2 = Image.open(p2name)
    temps1 = temperature1.getdata()
    temps2 = temperature2.getdata()
    precs1 = precipitation1.getdata()
    precs2 = precipitation2.getdata()
    rawData = zip(temps1, temps2, precs1, precs2)
    getRGBs = makeRGBConversion(temperature1, temperature2, precipitation1, precipitation2)
    if (mode == 'koppen'):
        newPix = [getClimateColor(getRGBs(pxTuple), tempProfile, precProfile, outProfile, idx < (len(temps1) / 2)) 
                  for idx, pxTuple in enumerate(rawData)]
    elif (mode == 'holdridge'):
        newPix = [getLifeZoneColor(getRGBs(pxTuple), tempProfile, precProfile, outProfile)
                  for idx, pxTuple in enumerate(rawData)]
    outputImg = Image.new('RGB', (temperature1.size[0], temperature1.size[1]))
    outputImg.putdata(newPix)
    return outputImg

# Lee un perfil de salida y verifica que todas sus claves sean clases Koppen válidas.
# También elimina el color 'Ocean' de la tabla de colores y lo convierte en el color ignorado
# si no se especificó uno (compatibilidad hacia atrás).
def readAndValidateKoppenOutputProfile(fname):
   profile = readOutputProfile(fname)
   
   for climate in profile.colorTable:
       if not (climate == 'Ocean'):
           if (not (climate in kColorTableDefault)):
               raise SKCCError('Invalid Köppen-Geiger class in output profile: ' + climate)
       else:
           if profile.ignoredColor != defaultOceanColor:
               profile.ignoredColor = profile.colorTable[climate]
   if ('Ocean' in profile.colorTable):
       profile.colorTable.pop(climate, None)
   return profile

# Lee un perfil de salida y verifica que todas sus claves sean zonas de Holdridge válidas.
# También elimina el color 'Océano' de la tabla de colores y lo utiliza como color ignorado
# si no se especificó ninguno (compatibilidad con versiones anteriores). 
def readAndValidateHoldridgeOutputProfile(fname):
    profile = readOutputProfile(fname)

    for zone in profile.colorTable:
        if not (zone == 'Ocean'):
            if (not (zone in hColorTableDefault)):
                raise SKCCError('Invalid Holdridge category in output profile: ' + zone)
        else:
            if profile.ignoredColor != defaultOceanColor:
                profile.ignoredColor = profile.colorTable[zone]
    if ('Ocean' in profile.colorTable):
        profile.colorTable.pop('Ocean', None)
    return profile

# Validates that a mode is a valid mode value.
def validateMode(md):
    if md in modes:
        return md
    else:
        raise SKCCError('Invalid mode specified: ' + mode) 



"""
# Begin script
if __name__ == '__main__':
    debug = False
    try:
        try:
            options, xarguments = getopt.getopt(sys.argv[1:], 'hvso:t:u:p:q:v:r:k:dm:', ['help', 'version', 'quiet', 'outfile=', 'tempnw=', 'tempns=', 'precnw=', 'precns=', 'tempprof=', 'precprof=', 'outprof=', 'debug', 'mode='])
        except getopt.error:
            optErr()

        startTime = time.time()

        tempFileNameNW = ''
        tempFileNameNS = ''
        precFileNameNW = ''
        precFileNameNS = ''
        outfileName = ''

        # El modo predeterminado del script es calcular los climas de Köppen-Geiger
        mode = 'koppen'
        
       # Configurar perfiles de color por defecto
        tempProfile = InputProfile(tColorTableDefault, [defaultOceanColor])
        precProfile = InputProfile(pColorTableDefault, [defaultOceanColor])

        outProfile = OutputProfile(kColorTableDefault, defaultOceanColor, defaultUnknownColor)

        quiet = False
        # Analiza las opciones: las banderas de depuración, ayuda, versión y modo deben estar antes o anulan
        # ciertas otras banderas, por lo que deben analizarse primero.

        for a in options[:]:
            if a[0] == '-d' or a[0] == '--debug':
                debug = True
        for a in options[:]:
            if a[0] == '-h' or a[0] == '--help':
                usage()
        for a in options[:]:
            if a[0] == '-v' or a[0] == '--version':
                version()
        for a in options[:]:
            if a[0] == '-m' or a[0] == '--mode':
                if a[1] == '':
                    optErr()
                else:
                    mode = validateMode(a[1])
                    if (mode == 'holdridge'):
                        outProfile = OutputProfile(hColorTableDefault, defaultOceanColor, defaultUnknownColor)
        for a in options[:]:
            if a[0] == '-o' or a[0] == '--outfile':
                if a[1] == '':
                    optErr()
                else:
                    outfileName = a[1]
            if a[0] == '-t' or a[0] == '--tempnw':
                if a[1] == '':
                    optErr()
                else:
                    tempFileNameNW = a[1]
            if a[0] == '-u' or a[0] == '--tempns':
                if a[1] == '':
                    optErr()
                else:
                    tempFileNameNS = a[1]
            if a[0] == '-p' or a[0] == '--precnw':
                if a[1] == '':
                    optErr()
                else:
                    precFileNameNW = a[1]
            if a[0] == '-q' or a[0] == '--precns':
                if a[1] == '':
                    optErr()
                else:
                    precFileNameNS = a[1]
            if a[0] == '-v' or a[0] == '--tempprof':
                if a[1] == '':
                    optErr()
                else:
                    tempProfile = readInputProfile(a[1])
            if a[0] == '-r' or a[0] == '--precprof':
                if a[1] == '':
                    optErr()
                else:
                    precProfile = readInputProfile(a[1])
            if a[0] == '-k' or a[0] == '--outprof':
                if a[1] == '':
                    optErr()
                else:
                    # Output profiles differ by mode
                    if (mode == 'koppen'):
                        outProfile = readAndValidateKoppenOutputProfile(a[1])
                    elif (mode == 'holdridge'):
                        outProfile = readAndValidateHoldridgeOutputProfile(a[1])
            if a[0] == '-s' or a[0] == '--quiet':
                quiet = True
        if ((not tempFileNameNS) or (not tempFileNameNW) or (not precFileNameNS) or (not precFileNameNW)):
            raise SKCCError('No se especificaron uno o más archivos de datos de entrada requeridos.')
        if (not outfileName):
            raise SKCCError('No se especificó un nombre de archivo de salida.')

        # generar el output.
        outputToFile(outfileName, buildOutput(tempFileNameNS, tempFileNameNW, precFileNameNS, precFileNameNW, tempProfile, precProfile, outProfile, mode))
        if not quiet:
            stopTime = time.time()
            timeDiffRounded = format(stopTime - startTime, '.2f')
            print('Output climate map to ' + outfileName + ' (' + timeDiffRounded + 's).')
    except Exception as e:
        # An error occurred.
        if (debug):
            # Mostrar el error con la traza de la pila si la bandera de depuración está activada.
            raise
        else:
            # Mostrar el error sin llenar la salida con la traza de la pila.
            print('Error: ' + str(e))

"""


# El modo predeterminado del script es calcular los climas de Köppen-Geiger
mode = 'koppen'

def koppen(mapa_temperatura,mapa_temperatura_mitad_año,mapa_presipitacion,mapa_presipitacion_mitad_año):

    kColorTableDefault = {'Af':(11, 36, 250), 'As':(76, 171, 247), 'Aw':(76, 171, 247), 'Am':(21, 123, 251), 
                'Cfa':(199, 253, 92), 'Csa':(255, 253, 56), 'Cwa':(153, 253, 154),
                'Cfb':(109, 253, 70), 'Csb':(198, 197, 41), 'Cwb':(103, 197, 104),
                'Cfc':(60, 197, 35), 'Csc':(198, 197, 41), 'Cwc':(103, 197, 104),
                'Dfa':(45, 255, 254), 'Dsa':(252, 40, 251), 'Dwa':(172, 179, 253),
                'Dfb':(66, 200, 252), 'Dsb':(196, 29, 197), 'Dwb':(92, 122, 216),
                'Dfc':(16, 126, 124), 'Dsc':(149, 55, 147), 'Dwc':(77, 84, 178),
                'Dfd':(6, 69, 93), 'Dsd':(149, 101, 148), 'Dwd':(50, 14, 133),
                'ET':(178, 178, 178), 'EF':(104, 104, 104),
                'BSh':(243, 162, 39), 'BSk':(254, 218, 108), 'BWh':(251, 13, 27), 'BWk':(252, 151, 151)}

    hColorTableDefault = {'Ice':(255, 255, 255), 'Polar desert':(214, 214, 214), 
                        'Subpolar dry tundra':(111, 131, 132), 'Subpolar moist tundra':(111, 131, 132),
                        'Subpolar wet tundra':(111, 131, 132), 'Subpolar rain tundra':(111, 131, 132), 
                        'Boreal desert':(222, 207, 143), 'Boreal dry scrub':(181, 180, 130),
                        'Boreal moist forest':(34, 96, 96), 'Boreal wet forest':(34, 96, 96), 
                        'Boreal rain forest':(34, 96, 96), 'Cool temperate desert':(222, 207, 143),
                        'Cool temperate desert scrub':(181, 180, 130), 'Cool temperate steppe':(85, 153, 84),
                        'Cool temperate moist forest':(27, 153, 119), 'Cool temperate wet forest':(27, 153, 119),
                        'Cool temperate rain forest':(27, 153, 119), 'Warm temperate desert':(254, 224, 92), 
                        'Warm temperate desert scrub':(194, 195, 101), 'Warm temperate thorn scrub':(132, 202, 90),
                        'Warm temperate dry forest':(132, 202, 90), 'Warm temperate moist forest':(32, 203, 126), 
                        'Warm temperate wet forest':(32, 203, 126), 'Warm temperate rain forest':(32, 203, 126),
                        'Subtropical desert':(254, 224, 92), 'Subtropical desert scrub':(194, 195, 101), 
                        'Subtropical thorn woodland':(202, 232, 94), 'Subtropical dry forest':(94, 230, 95),
                        'Subtropical moist forest':(94, 230, 95), 'Subtropical wet forest':(41, 177, 72), 
                        'Subtropical rain forest':(41, 177, 72), 'Tropical desert':(254, 224, 92),
                        'Tropical desert scrub':(194, 195, 101), 'Tropical thorn woodland':(202, 232, 94), 
                        'Tropical very dry forest':(202, 232, 94), 'Tropical dry forest':(94, 230, 95),
                        'Tropical moist forest':(41, 177, 72), 'Tropical wet forest':(41, 177, 72), 
                        'Tropical rain forest':(41, 177, 72)}

    tColorTableDefault = {(160, 0, 65):38, (210, 60, 80):31, (245, 110, 65):25, (250, 175, 95):20,
                (255, 225, 140):14, (230, 245, 150):5, (170, 220, 165):-5, (100, 195, 165):-18,
                (50, 135, 190):-32, (95, 80, 160):-40}

    pColorTableDefault = {(135, 0, 180):300.0, (130, 60, 200):170.0, (105, 70, 200):105.0, (60, 60, 180):55.0, 
                (70, 95, 150):30.0, (55, 85, 100):15.0, (35, 50, 50):7.5, (20, 20, 20):2.5}

    defaultOceanColor = (107, 165, 210)

    defaultUnknownColor = (0, 0, 0)
    outProfile = OutputProfile(kColorTableDefault, defaultOceanColor, defaultUnknownColor)

    mode = 'koppen'

    tempProfile,precProfile = defprofile()


    #outputToFile(outfileName, buildOutput(mapa_temperatura,mapa_temperatura_mitad_año,mapa_presipitacion,mapa_presipitacion_mitad_año, tempProfile, precProfile, outProfile, mode))
    imagen = buildOutput(mapa_temperatura,mapa_temperatura_mitad_año,mapa_presipitacion,mapa_presipitacion_mitad_año, tempProfile, precProfile, outProfile, mode)
    return imagen

