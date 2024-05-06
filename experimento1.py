""" Esta es mi validación """

from pathlib import Path
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from bordes_geograficos import BordesGeograficos

def cambiar_extension(archivo_jpg):
    """ cambia nombre """
    nombre= os.path.splitext(archivo_jpg)[0]
    nuevo_nombre=nombre + ".txt"
    return nuevo_nombre

def sexa_to_dec(coord):
    """ Convierte coordenadas sexagesimales a decimales """
    degrees, minutes, seconds = coord
    dec = degrees + minutes / 60 + seconds / 3600
    return dec

def extremos(coordenadas):
    """ encuentra puntos extremos y cambia a decimales """
    lat_min = coordenadas[0][0]
    lat_max = coordenadas[0][2]
    lon_min = coordenadas[0][0]
    lon_max = coordenadas[0][2]

    lat_min_coord = coordenadas[0]
    lat_max_coord = coordenadas[0]
    lon_min_coord = coordenadas[0]
    lon_max_coord = coordenadas[0]

    for coord in coordenadas:
        if coord[0] < lat_min:
            lat_min = coord[0]
            lat_min_coord = coord
        if coord[0] > lat_max:
            lat_max = coord[0]
            lat_max_coord = coord
        if coord[2] < lon_min:
            lon_min = coord[2]
            lon_min_coord = coord
        if coord[2] > lon_max:
            lon_max = coord[2]
            lon_max_coord = coord

    lat_min_coord = (
        round(sexa_to_dec(lat_min_coord[0]), 5), lat_min_coord[1],
        round(sexa_to_dec(lat_min_coord[2]), 5)
        )
    lat_max_coord = (
        round(sexa_to_dec(lat_max_coord[0]), 5),
        lat_max_coord[1], round(sexa_to_dec(lat_max_coord[2]), 5)
        )
    lon_min_coord = (
        round(sexa_to_dec(lon_min_coord[0]), 5),
        lon_min_coord[1], round(sexa_to_dec(lon_min_coord[2]), 5)
        )
    lon_max_coord = (
        round(sexa_to_dec(lon_max_coord[0]), 5), lon_max_coord[1],
        round(sexa_to_dec(lon_max_coord[2]), 5)
        )

    return {
        'latitud_minima': lat_min_coord,
        'latitud_maxima': lat_max_coord,
        'longitud_minima': lon_min_coord,
        'longitud_maxima': lon_max_coord
    }

if __name__ == '__main__':
    imagenes_path = Path().absolute().parent / "practica_datagricola/imagenes"
    lista_images = os.listdir(imagenes_path)

    extremos_imagenes = []

    for imagen in lista_images:
        imagen_path = imagenes_path.joinpath(imagen)
        my_instance = BordesGeograficos(
            path=str(imagen_path),
            dim_sensor=(6.4, 4.8)
        )
        coordenadas_imagen = my_instance.main()
        for tup in coordenadas_imagen:
            print(tup[0],tup[2])
        puntos_extremos = extremos(coordenadas_imagen)
        extremos_imagenes.append(puntos_extremos)

    lats_min = min(extremos_imagenes, key=lambda x: x['latitud_minima'][0])['latitud_minima']
    lats_max = max(extremos_imagenes, key=lambda x: x['latitud_maxima'][0])['latitud_maxima']
    lons_min = min(extremos_imagenes, key=lambda x: x['longitud_minima'][2])['longitud_minima']
    lons_max = max(extremos_imagenes, key=lambda x: x['longitud_maxima'][2])['longitud_maxima']

    for image in lista_images:
        nuevo_archivo=cambiar_extension(image)
      # print("El nuevo nombre del archivo es:", nuevo_archivo)
        with open(nuevo_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write()

    extremos_finales = {
        'latitud_minima': lats_min,
        'latitud_maxima': lats_max,
        'longitud_minima': lons_min,
        'longitud_maxima': lons_max
    }


    plt.scatter(
        [lats_min[2], lats_max[2], lons_min[2], lons_max[2]],
        [lats_min[0], lats_max[0], lons_min[0], lons_max[0]],
        color='red', marker='o'
    )

    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.title('Puntos Extremos')
    plt.grid(True)
    plt.savefig('puntos_extremos.png')

    cols = int((lons_max[2] - lons_min[2]) / 0.1) + 1
    rows = int((lats_max[0] - lats_min[0]) / 0.1) + 1
    ortofoto = np.zeros((rows, cols))
    fig, ax = plt.subplots()

    for puntos in extremos_imagenes:
        lat_mins = puntos['latitud_minima'][0]
        lat_maxs = puntos['latitud_maxima'][0]
        lon_mins = puntos['longitud_minima'][2]
        lon_maxs = puntos['longitud_maxima'][2]

        rect = Polygon(
            [(lon_mins, lat_mins),
            (lon_maxs, lat_mins),
            (lon_maxs, lat_maxs),
            (lon_mins, lat_maxs)
            ], closed=True
        )

        ax.add_patch(rect)

        mask = (
            lats_min[0] <= lat_mins
            ) & (
                lat_mins <= lats_max[0]
                ) & (
                    lons_min[2] <= lon_mins
                    ) & (
                        lon_mins <= lons_max[2]
                        ) #Crea la máscara
        rows_idx = np.arange(rows)[mask]
        cols_idx = np.arange(cols)[mask]

        ortofoto[rows_idx[:, None], cols_idx] = 1

    ax.imshow(ortofoto, extent=(
        lons_min[2], lons_max[2], lats_min[0], lats_max[0]
    ), cmap='gray', origin='lower')

    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.title('Ortofoto')
    plt.grid(True)
    plt.savefig('ortofoto.png')
