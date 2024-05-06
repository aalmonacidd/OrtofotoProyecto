""" otra validacion """
from pathlib import Path
import os
from bordes_geograficos import BordesGeograficos

imagenes_path = Path().absolute().parent / "practica_datagricola/imagenes"
lista_images = os.listdir(imagenes_path)

def cambiar_extension(archivo_jpg):
    """ cambia nombre """
    nombre= os.path.splitext(archivo_jpg)[0]
    nuevo_nombre=nombre + ".txt"
    return nuevo_nombre

for image in lista_images:
    nuevo_archivo=cambiar_extension(image)
    print("El nuevo nombre del archivo es:", nuevo_archivo)
