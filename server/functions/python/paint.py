import cv2
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

celesteBajo = np.array([75, 185, 88], np.uint8)
celesteAlto = np.array([112, 255, 255], np.uint8)

# Colores para pintar
colorCeleste = (255, 113, 82)
colorAmarillo = (89, 222, 255)
colorRosa = (128, 0, 255)
colorVerde = (0, 255, 36)

# Solo se usará para el cuadro superior de 'Limpiar Pantalla'
colorLimpiarPantalla = (29, 112, 246)

# Grosor de línea recuadros superior izquierda (color a dibujar)
grosorCeleste = 6
grosorAmarillo = 2
grosorRosa = 2
grosorVerde = 2

# Grosor de línea recuadros superior derecha (grosor del marcador para dibujar)
grosorPeque = 6
grosorMedio = 1
grosorGrande = 1

# --------------------- Variables para el marcador / lápiz virtual -------------------------
color = colorCeleste  # Color de entrada, y variable que asignará el color del marcador
grosor = 3  # Grosor que tendrá el marcador

# ------------------------------------------------------------------------------------------
x1 = None
y1 = None
imAux = None
