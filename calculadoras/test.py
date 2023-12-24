"""
problema

crear una funcion que me cree un collague con el mapa original a un tamaño x 

input: puntos opuestos de las cuadriculas, ubicacion del proyecto, tamaño de las imagenes.

output: collage echo, ubicacion del proyecto, informacion de cada subdivicion de la imagen y en donde lo tiene que guardar y que nombre tienen


"""

from PIL import Image

# como funciona la funcion

"""
1-- calcula todas las imagenes que estan dentro de los 2 puntos que ingresamos

2-- identificar quienes son las imagenes de nivel superior a lo cuales conforman
   crear una lista con todas las imagenes posibles 

3-- usar la lista para identificar cuales de las imagenes existen y cuales 
    son las que tenemos que recortar y separar las listas en imagenes existentes y magenes que no existen

4-- recortar y guardar las imagenes 

5-- crear un collague con las imagenes

6-- crear un json con la informacion de las subdiviciones de las imagenes

7-- guardar el json y el collage

"""

# 1-- 

"""
crear una funcion que me retorne una lista con los nombres  de cada imagen que 
pertenezcan a la cuadricula creada por dos puntos (l x y) como inputs

casos limites son en los extremos de las cuadriculas por ejemplo en los x minimos y x maximos en donde el punto a es el x maximo y el punto b es el x minimo
esto tiene que solucionarse que cuando x llega a su maximo este regrese a 0 y continue contando
"""





# 2-- ya creado
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

# 3--
"""
se tiene que navegar por las carpetas e identificar desde los niveles 
superiores a niveles inferiores que imagenes existen para aprovecharlos 

crear 2 listas por nivel

lista1 de iamgenes existentes con l x y
lista2 de imagenes que no existen 

"""



# 4--
"""
tienen que ingresar la lista de imagenes y subdicidir las imagenes en 4 y guardarlos en una lista nueva
y si la lista de imagenes existentes no esta vacia, agregar esa imagen a la lista de salida y solo retornar una unica lista 
"""


# 5--
"""
una ves recorrido toda la lista y las imagenes finales ya esten lista en una sola lista crear un collage de la lista y guardarlo
"""


carpeta = r"F:\\obsidian\\ProyectoReinado\\Recursos\\imagenes\\mapa"
imagenr = carpeta + "\\" + "52.png"

guardar = carpeta + "\\" + "test"

imagenes = Image.open(imagenr)

ancho,alto = imagenes.size

ancho2= ancho/2
alto2 = alto/2

imagen_a = imagenes.crop((0, 0, ancho2, alto2))
imagen_b = imagenes.crop((ancho2, 0, ancho, alto2))
imagen_c = imagenes.crop((0, alto2, ancho2, alto))
imagen_d = imagenes.crop((ancho2, alto2, ancho, alto))


print(imagen_a)
print(imagen_b)
print(imagen_c)
print(imagen_d)