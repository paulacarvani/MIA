# Importamos las librerias
import cv2
import random
import hands as sm  # Clase manos
import os
import imutils


fs = False
fu = False      # Bandera up
fd = False      # Bandera down
fj = False      # Bandera juego
fr = False      # Bandera reset
fgia = False    # Bandera gana IA
fgus = False    # Bandera gana Usuario
femp = False    # Bandera empate
fder = False    # Bandera derecha
fizq = False    # Bandera izquierda
conteo = 0


path = 'Imagenes'
images = []
clases = []
lista = os.listdir(path)


# The above code is reading images from a directory specified by the `path` variable and appending
# them to a list called `images`. It is also extracting the class labels from the filenames and
# appending them to another list called `clases`. The code assumes that the images are in the format
# of a list called `lista`. The `cv2.imread()` function is used to read the images using the OpenCV
# library. The `os.path.splitext()` function is used to extract the filename without the extension,
# which is assumed to be the class label.
for lis in lista:
    imgdb = cv2.imread(f'{path}/{lis}')
    images.append(imgdb)
    clases.append(os.path.splitext(lis)[0])

print(images)


# The above code is initializing a video capture object in OpenCV with the default camera (index 0).
# This object can be used to capture frames from the camera for further processing or analysis.
cap = cv2.VideoCapture(0)


# The above code is not valid Python code. It seems to be incomplete and contains a syntax error.
detector = sm.detectormanos(Confdeteccion=0.9)


# The above code is reading frames from a video capture device using OpenCV. It then waits for a key
# press event, finds the dimensions of the frame, flips the frame horizontally, and detects hands in
# the frame using a hand detection model. It then finds the position of the hand and draws a bounding
# box around it. The variables `lista1`, `bbox1`, and `jug` contain information about the hand
# position and gesture. The code runs in an infinite loop until the user interrupts it.
while True:
    ret, frame = cap.read()
    t = cv2.waitKey(1)
    al, an, c = frame.shape
    cx = int(an/2)
    cy = int(al/2)
    frame = cv2.flip(frame,1)
    frame = detector.encontrarmanos(frame, dibujar=True)
    lista1, bbox1, jug = detector.encontrarposicion(frame, ManoNum=0, dibujar=True, color = [0,255,0])

    # 1 Jugador
    if jug == 1:
        cv2.line(frame, (cx,0), (cx,480), (0,255,0), 2)

        cv2.rectangle(frame, (245, 25), (380, 60), (0, 0, 0), -1)
        cv2.putText(frame, '1 JUGADOR', (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.71,(0, 255, 0), 2)

        cv2.rectangle(frame, (145, 425), (465, 460), (0, 0, 0), -1)
        cv2.putText(frame, 'PRESIONA S PARA EMPEZAR', (150, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (0, 255, 0), 2)

        # Presiona S
        if t == 83 or t == 115 or fs == True:
            # Cambiamos bandera 's'
            fs = True
            if len(lista1) != 0:
                x1, y1 = lista1[9][1:]

                if conteo <= 2:
                    img = images[conteo]
                    img = imutils.resize(img, width=240, height=240)
                    ali, ani, c = img.shape

                    if x1 < cx:
                        fizq = True
                        fder = False
                        frame[130: 130 + ali, 350: 350 + ani] = img

                        if y1 < cy - 40 and fd == False:
                            fu = True
                            cv2.circle(frame, (cx, cy), 5, (255, 255, 0), -1)

                        elif y1 > cy - 40 and fu == True:
                            conteo = conteo + 1
                            fu = False

                    # Derecha
                    elif x1 > cx:
                        fder = True
                        fizq = False
                        frame[130: 130 + ali, 30: 30 + ani] = img

                        if y1 < cy - 40 and fd == False:
                            fu = True
                            cv2.circle(frame, (cx,cy), 5, (255,255,0), -1)

                        elif y1 > cy - 40 and fu == True:
                            conteo = conteo + 1
                            fu = False
                # Jugamos
                elif conteo == 3:
                    # Si no hemos jugado jugamos
                    if fj == False and fr == False:
                        # Elegimos piedra papel o tijera
                        juego = random.randint(3,5)
                        fj = True

                    # Izquierda
                    if fizq == True and fder == False:
                        # Mostramos
                        img = images[juego]
                        # Redimensionamos
                        img = imutils.resize(img, width=240, height=240)
                        ali, ani, c = img.shape
                        # Mostramos imagen
                        frame[130: 130 + ali, 350: 350 + ani] = img
                        print(juego)

                        # Si ya jugamos
                        if fj == True and fr == False:
                            # Extraemos valores de interes
                            # Punta DI
                            x2, y2 = lista1[8][1:]
                            # Punta DC
                            x3, y3 = lista1[12][1:]
                            # Punta DA
                            x4, y4 = lista1[16][1:]

                            # Falange DI
                            x22, y22 = lista1[6][1:]
                            # Falange DC
                            x33, y33 = lista1[10][1:]
                            # Falange DA
                            x44, y44 = lista1[14][1:]

                            # Condiciones de posicion
                            # Piedra
                            if x2 < x22 and x3 < x33 and x4 < x44:
                                # IA PAPEL
                                if juego == 3:
                                    # GANA IA
                                    print('GANA LA IA')
                                    # Bandera Ganador
                                    fgia = True
                                    fgus = False
                                    femp = False
                                    fr = True
                                # IA PIEDRA
                                elif juego == 4:
                                    # EMPATE
                                    print('EMPATE')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = False
                                    femp = True
                                    fr = True

                                elif juego == 5:
                                    # GANA USUARIO
                                    print('GANA EL HUMANO')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = True
                                    femp = False
                                    fr = True


                            # Papel
                            elif x2 > x22 and x3 > x33 and x4 > x44:
                                # IA PAPEL
                                if juego == 3:
                                    # EMPATE
                                    print('EMPATE')
                                    fgia = False
                                    fgus = False
                                    fr = True
                                    femp = True
                                # IA PIEDRA
                                elif juego == 4:
                                    # GANA USUARIO
                                    print('GANA EL HUMANO')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = True
                                    femp = False
                                    fr = True
                                elif juego == 5:
                                    # GANA LA IA
                                    print('GANA LA IA')
                                    # Bandera Ganador
                                    fgia = True
                                    fgus = False
                                    femp = False
                                    fr = True

                            # Tijera
                            elif x2 > x22 and x3 > x33 and x4 < x44:
                                # IA PAPEL
                                if juego == 3:
                                    # GANA EL USUARIO
                                    print('GANA EL HUMANO')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = True
                                    femp = False
                                    fr = True
                                # IA PIEDRA
                                elif juego == 4:
                                    # GANA LA IA
                                    print('GANA LA IA')
                                    # Bandera Ganador
                                    fgia = True
                                    fgus = False
                                    femp = False
                                    fr = True
                                elif juego == 5:
                                    # EMPATE
                                    print('EMPATE')
                                    fgia = False
                                    fgus = False
                                    femp = True
                                    fr = True

                        # Mostramos ganador
                        # IA
                        if fgia == True:
                            # Mostramos
                            gan = images[6]
                            alig, anig, c = gan.shape
                            # Mostramos imagen
                            frame[70: 70 + alig, 180: 180 + anig] = gan

                            # Reset
                            if t == 82 or t == 114:
                                fs = False
                                fu = False
                                fd = False
                                fj = False
                                fr = False
                                fgia = False
                                fgus = False
                                femp = False
                                fder = False
                                fizq = False
                                conteo = 0

                        # USUARIO
                        elif fgus == True:
                            # Mostramos
                            gan = images[7]
                            alig, anig, c = gan.shape
                            # Mostramos imagen
                            frame[70: 70 + alig, 180: 180 + anig] = gan

                            # Reset
                            if t == 82 or t == 114:
                                fs = False
                                fu = False
                                fd = False
                                fj = False
                                fr = False
                                fgia = False
                                fgus = False
                                femp = False
                                fder = False
                                fizq = False
                                conteo = 0

                        # EMPATE
                        elif femp == True:
                            # Mostramos
                            gan = images[8]
                            alig, anig, c = gan.shape
                            # Mostramos imagen
                            frame[70: 70 + alig, 180: 180 + anig] = gan

                            # Reset
                            if t == 82 or t == 114:
                                fs = False
                                fu = False
                                fd = False
                                fj = False
                                fr = False
                                fgia = False
                                fgus = False
                                femp = False
                                fder = False
                                fizq = False
                                conteo = 0


                    # Derecha
                    if fizq == False and fder == True:
                        # Mostramos
                        img = images[juego]
                        # Redimensionamos
                        img = imutils.resize(img, width=240, height=240)
                        ali, ani, c = img.shape
                        # Mostramos imagen
                        frame[130: 130 + ali, 30: 30 + ani] = img
                        print(juego)

                        # Si ya jugamos
                        if fj == True and fr == False:
                            # Extraemos valores de interes
                            # Punta DI
                            x2, y2 = lista1[8][1:]
                            # Punta DC
                            x3, y3 = lista1[12][1:]
                            # Punta DA
                            x4, y4 = lista1[16][1:]

                            # Falange DI
                            x22, y22 = lista1[6][1:]
                            # Falange DC
                            x33, y33 = lista1[10][1:]
                            # Falange DA
                            x44, y44 = lista1[14][1:]

                            # Condiciones de posicion
                            # Piedra
                            if x2 > x22 and x3 > x33 and x4 > x44:
                                # IA PAPEL
                                if juego == 3:
                                    # GANA IA
                                    print('GANA LA IA')
                                    # Bandera Ganador
                                    fgia = True
                                    fgus = False
                                    femp = False
                                    fr = True
                                # IA PIEDRA
                                elif juego == 4:
                                    # EMPATE
                                    print('EMPATE')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = False
                                    femp = True
                                    fr = True

                                elif juego == 5:
                                    # GANA USUARIO
                                    print('GANA EL HUMANO')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = True
                                    femp = False
                                    fr = True


                            # Papel
                            elif x2 < x22 and x3 < x33 and x4 < x44:
                                # IA PAPEL
                                if juego == 3:
                                    # EMPATE
                                    print('EMPATE')
                                    fgia = False
                                    fgus = False
                                    fr = True
                                    femp = True
                                # IA PIEDRA
                                elif juego == 4:
                                    # GANA USUARIO
                                    print('GANA EL HUMANO')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = True
                                    femp = False
                                    fr = True
                                elif juego == 5:
                                    # GANA LA IA
                                    print('GANA LA IA')
                                    # Bandera Ganador
                                    fgia = True
                                    fgus = False
                                    femp = False
                                    fr = True

                            # Tijera
                            elif x2 < x22 and x3 < x33 and x4 > x44:
                                # IA PAPEL
                                if juego == 3:
                                    # GANA EL USUARIO
                                    print('GANA EL HUMANO')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = True
                                    femp = False
                                    fr = True
                                # IA PIEDRA
                                elif juego == 4:
                                    # GANA LA IA
                                    print('GANA LA IA')
                                    # Bandera Ganador
                                    fgia = True
                                    fgus = False
                                    femp = False
                                    fr = True
                                elif juego == 5:
                                    # EMPATE
                                    print('EMPATE')
                                    fgia = False
                                    fgus = False
                                    femp = True
                                    fr = True

                        # Mostramos ganador
                        # IA
                        if fgia == True:
                            # Mostramos
                            gan = images[6]
                            alig, anig, c = gan.shape
                            # Mostramos imagen
                            frame[70: 70 + alig, 180: 180 + anig] = gan

                            # Reset
                            if t == 82 or t == 114:
                                fs = False
                                fu = False
                                fd = False
                                fj = False
                                fr = False
                                fgia = False
                                fgus = False
                                femp = False
                                fder = False
                                fizq = False
                                conteo = 0

                        # USUARIO
                        elif fgus == True:
                            # Mostramos
                            gan = images[7]
                            alig, anig, c = gan.shape
                            # Mostramos imagen
                            frame[70: 70 + alig, 180: 180 + anig] = gan

                            # Reset
                            if t == 82 or t == 114:
                                fs = False
                                fu = False
                                fd = False
                                fj = False
                                fr = False
                                fgia = False
                                fgus = False
                                femp = False
                                fder = False
                                fizq = False
                                conteo = 0

                        # EMPATE
                        elif femp == True:
                            # Mostramos
                            gan = images[8]
                            alig, anig, c = gan.shape
                            # Mostramos imagen
                            frame[70: 70 + alig, 180: 180 + anig] = gan

                            # Reset
                            if t == 82 or t == 114:
                                fs = False
                                fu = False
                                fd = False
                                fj = False
                                fr = False
                                fgia = False
                                fgus = False
                                femp = False
                                fder = False
                                fizq = False
                                conteo = 0

    # 2 Jugadores
    elif jug == 2:
        # Encontramos la segunda mano
        lista2, bbox2, jug2 = detector.encontrarposicion(frame, ManoNum=1, dibujar=True, color = [255,0,0])

        # Dividimos pantalla
        cv2.line(frame, (cx, 0), (cx, 240), (255, 0, 0), 2)
        cv2.line(frame, (cx, 240), (cx, 480), (0, 255, 0), 2)

        # Mostramos jugadores
        cv2.rectangle(frame, (245, 25), (408, 60), (0, 0, 0), -1)
        cv2.putText(frame, '2 JUGADORES', (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (255, 0, 0), 2)

        # Mensaje inicio
        cv2.rectangle(frame, (145, 425), (465, 460), (0, 0, 0), -1)
        cv2.putText(frame, 'PRESIONA S PARA EMPEZAR', (150, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (255, 0, 0), 2)

        if t == 83 or t == 115:
            print('EMPEZAMOS')

    # 0 Jugadores
    elif jug == 0:
        # Mostramos jugadores
        cv2.rectangle(frame, (225, 25), (388, 60), (0, 0, 0), -1)
        cv2.putText(frame, '0 JUGADORES', (230, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (0, 0, 255), 2)

        # Mensaje inicio
        cv2.rectangle(frame, (115, 425), (480, 460), (0, 0, 0), -1)
        cv2.putText(frame, 'LEVANTA TU MANO PARA INICIAR', (120, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (0, 0, 255), 2)


    # Mostramos frames
    cv2.imshow("JUEGO CON AI", frame)
    if t == 27:
        break
cap.release()
cv2.destroyAllWindows()
