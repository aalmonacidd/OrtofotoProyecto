"""Descripcion del modulo"""

from exif import Image

class BordesGeograficos:
    """Aqui va algo!"""
    def __init__(self, path, dim_sensor: tuple):
        self.path = path
        self.dim_sensor = dim_sensor
        self.imagen = None

    def read_image(self):
        """Este metodo lee la imagen"""
        with open(self.path, 'rb') as img:
            self.imagen = Image(img)
        return self.imagen

    @staticmethod
    def conv_sec(metros):
        """Función para convertir metros a segundos"""
        return round(int(metros / (1850 / 60)), 1)
    def calcular_distancia(self):
        """Aplica el teorema de Tales para calcular la longitud de la imagen"""
        xlong_ = (
            ((self.dim_sensor[0] / 2) * self.imagen.gps_altitude)
            / self.imagen.focal_length
        )
        ylong_ = (
            ((self.dim_sensor[1] / 2) * self.imagen.gps_altitude)
            / self.imagen.focal_length
        )
        return round(xlong_, 1), round(ylong_, 1)

    @staticmethod
    def calc_sexagesimal(coor: tuple, s: float, operacion=None):
        """Operaciones con coordenadas sexagesimales"""
        if operacion == 'suma':
            if coor[2] + s > 60:
                sec = 0
                if coor[1] + 1 > 60:
                    min_ = 0
                    deg = coor[0] + 1
                else:
                    min_ = coor[1] + 1
                    deg = coor[0]
            else:
                sec = coor[2] + s
                min_ = coor[1]
                deg = coor[0]
            return (round(deg, 1), round(min_, 1), round(sec, 1))
        else:
            if coor[2] - s < 0:
                sec = 60
                if coor[1] - 1 < 0:
                    min_ = 60
                    deg = coor[0] - 1
                else:
                    min_ = coor[0] - 1
                    deg = coor[0]
            else:
                sec = coor[2] - s
                min_ = coor[1]
                deg = coor[0]
            return (round(deg, 1), round(min_, 1), round(sec, 1))

    def main(self):
        """Esto es lo que define el trabajo de la clase ..."""
        self.read_image()
        sum_lon = (BordesGeograficos.calc_sexagesimal(
            self.imagen.gps_longitude, BordesGeograficos.conv_sec(
                self.calcular_distancia()[0]
                ),
                'suma'
            )
        )
        # Resta los segundos a la longitud del centroide
        res_lon = (BordesGeograficos.calc_sexagesimal(
            self.imagen.gps_longitude, BordesGeograficos.conv_sec(
                self.calcular_distancia()[0]
                )
            )
        )
        # Suma los segundos a la longitud del centroide
        sum_lat = (BordesGeograficos.calc_sexagesimal(
            self.imagen.gps_latitude, BordesGeograficos.conv_sec(
                self.calcular_distancia()[1]
                ),
                'suma'
            )
        )
        # Resta los segundos a la longitud del centroide
        res_lat = (BordesGeograficos.calc_sexagesimal(
            self.imagen.gps_latitude, BordesGeograficos.conv_sec(
                self.calcular_distancia()[1]
                )
            )
        )
        a = (sum_lon, self.imagen.gps_longitude_ref, res_lat, self.imagen.gps_latitude_ref)
        b = (sum_lon, self.imagen.gps_longitude_ref, sum_lat, self.imagen.gps_latitude_ref)
        c = (res_lon, self.imagen.gps_longitude_ref, res_lat, self.imagen.gps_latitude_ref)
        d = (res_lon, self.imagen.gps_longitude_ref, sum_lat, self.imagen.gps_latitude_ref)

        return a,b,c,d

#print(__name__)
if __name__ == '__main__':
    print("Hola mundo desde bordes geograficos!!!")

