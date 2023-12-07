import ctypes
import numpy as np

# Cargar la biblioteca compartida (SO)
erodr_dll = ctypes.CDLL('F:\programacion\python\Mapa_de_fantasia\Fantasy_Map_Helper\calculadoras\erodr-master\src\liberodr.dll')

# Declarar el tipo de argumentos y el tipo de retorno de la función
erodr_dll.simulate_particles.argtypes = [
    np.ctypeslib.ndpointer(dtype=np.double, ndim=2, flags='C_CONTIGUOUS'),  # hmap
    ctypes.c_int,  # width
    ctypes.c_int,  # height
    ctypes.c_int,  # n
    ctypes.c_int,  # ttl
    ctypes.c_double,  # p_enertia
    ctypes.c_double,  # p_min_slope
    ctypes.c_double,  # p_capacity
    ctypes.c_double,  # p_deposition
    ctypes.c_double,  # p_erosion
    ctypes.c_int,  # p_radius
    ctypes.c_double,  # p_gravity
    ctypes.c_double  # p_evaporation
]
erodr_dll.simulate_particles.restype = None

# Utilizar la función en Python
height, width = 10, 10  # Asegúrate de tener un mapa de alturas válido
hmap = np.zeros((height, width), dtype=np.double)
erodr_dll.simulate_particles(hmap, width, height, 10, 100, 0.1, 0.01, 0.1, 0.01, 0.01, 3, 9.8, 0.01)
print(hmap)
