import math
import cv2
import mediapipe as mp
import time


class detectormanos():
    def __init__(self, mode=False, maxManos = 2, model_complexity=1, Confdeteccion = 0.5, Confsegui = 0.5):
        """
        This function initializes an object with various parameters for hand detection and tracking
        using the MediaPipe library in Python.
        
        :param mode: A boolean value that determines whether to detect hands in a static image or in
        real-time video stream, defaults to False (optional)
        :param maxManos: The maximum number of hands to detect. By default, it is set to 2, which means
        the code can detect up to two hands at a time, defaults to 2 (optional)
        :param model_complexity: refers to the complexity of the hand tracking model being used. A
        higher value means a more complex model with potentially better accuracy but also higher
        computational requirements, defaults to 1 (optional)
        :param Confdeteccion: It is the confidence threshold for hand detection. If the confidence score
        of a detected hand is below this threshold, it will not be considered as a valid detection
        :param Confsegui: Confsegui is a float value representing the minimum confidence score required
        for a hand landmark to be considered as detected and tracked by the MediaPipe Hands model. The
        default value is 0.5, which means that the model will only consider landmarks with a confidence
        score of 0.5 or higher
        """
        self.mode = mode
        self.maxManos = maxManos
        self.compl = model_complexity
        self.Confdeteccion = Confdeteccion
        self.Confsegui = Confsegui

        self.mpmanos = mp.solutions.hands
        self.manos = self.mpmanos.Hands(self.mode, self.maxManos, self.compl, self.Confdeteccion, self.Confsegui)
        self.dibujo = mp.solutions.drawing_utils
        self.tip = [4,8,12,16,20]

    def encontrarmanos(self, frame, dibujar = True ):
        """
        This function detects and draws landmarks on hands in a given frame using the MediaPipe Hands
        library in Python.
        
        :param frame: The input image frame on which the hand detection and landmark detection is
        performed
        :param dibujar: It is a boolean parameter that determines whether to draw the landmarks and
        connections on the frame or not. If it is set to True, the landmarks and connections will be
        drawn on the frame, otherwise, they will not be drawn, defaults to True (optional)
        :return: the input frame with the detected hand landmarks and connections drawn on it.
        """
        imgcolor = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.resultados = self.manos.process(imgcolor)

        if self.resultados.multi_hand_landmarks:
            for mano in self.resultados.multi_hand_landmarks:
                if dibujar:
                    self.dibujo.draw_landmarks(frame, mano, self.mpmanos.HAND_CONNECTIONS)  # Dibujamos las conexiones de los puntos
        return frame


    def encontrarposicion(self, frame, ManoNum = 0, dibujar = True, color = []):
        """
        This function finds the position of a hand in a frame and returns the coordinates and bounding
        box, and can also draw the hand and bounding box on the frame.

        :param frame: The current frame of the video being processed
        :param ManoNum: The index of the hand to be detected and tracked. If there are multiple hands in
        the frame, this parameter can be used to select a specific hand. The default value is 0, which
        means the first hand in the list of detected hands will be selected, defaults to 0 (optional)
        :param dibujar: It is a boolean parameter that determines whether to draw circles and rectangles
        on the frame or not. If set to True, it will draw circles and rectangles on the frame, and if
        set to False, it will not draw anything, defaults to True (optional)
        :param color: The color parameter is used to specify the color of the rectangle that is drawn
        around the hand landmarks. It is an optional parameter and if not specified, the default color
        is used
        :return: a tuple with three elements:
        1. A list of lists containing the id, x and y coordinates of each landmark detected in the hand.
        2. A tuple with the coordinates of the bounding box that encloses the hand.
        3. An integer representing the number of hands detected in the frame.
        """
        xlista = []
        ylista = []
        bbox = []
        player = 0
        self.lista = []
        if self.resultados.multi_hand_landmarks:
            miMano = self.resultados.multi_hand_landmarks[ManoNum]
            prueba = self.resultados.multi_hand_landmarks
            player = len(prueba)
            #print(player)
            for id, lm in enumerate(miMano.landmark):
                alto, ancho, c = frame.shape  # Extraemos las dimensiones de los fps
                cx, cy = int(lm.x * ancho), int(lm.y * alto)  # Convertimos la informacion en pixeles
                xlista.append(cx)
                ylista.append(cy)
                self.lista.append([id, cx, cy])
                if dibujar:
                    cv2.circle(frame,(cx, cy), 3, (0, 0, 0), cv2.FILLED)  # Dibujamos un circulo

            xmin, xmax = min(xlista), max(xlista)
            ymin, ymax = min(ylista), max(ylista)
            bbox = xmin, ymin, xmax, ymax
            if dibujar:
                # Dibujamos cuadro
                cv2.rectangle(frame,(xmin - 20, ymin - 20), (xmax + 20, ymax + 20), color,2)
        return self.lista, bbox, player


    def dedosarriba(self):
        """
        This function returns a list of 5 binary values indicating whether each finger should be up (1) or
        down (0) based on the position of certain points in a hand.
        :return: The function `dedosarriba` returns a list of integers representing whether each finger is
        raised (1) or not (0) based on the position of the fingers in the `self.lista` list.
        """
        dedos = []
        if self.lista[self.tip[0]][1] > self.lista[self.tip[0]-1][1]:
            dedos.append(1)
        else:
            dedos.append(0)

        for id in range (1,5):
            if self.lista[self.tip[id]][2] < self.lista[self.tip[id]-2][2]:
                dedos.append(1)
            else:
                dedos.append(0)

        return dedos


    def distancia(self, p1, p2, frame, dibujar = True, r = 15, t = 3):
        """
        This function calculates the distance between two points and draws circles and lines on an image
        to visualize the points and distance.
        
        :param p1: The index of the first point in the list of points
        :param p2: p2 is the index of the second point in the list of points stored in the object
        calling the "distancia" method
        :param frame: The current frame of the video being processed
        :param dibujar: This is a boolean parameter that determines whether or not to draw the distance
        and circles on the frame. If set to True, the function will draw the distance and circles on the
        frame. If set to False, it will not draw anything on the frame, defaults to True (optional)
        :param r: The radius of the circles drawn around the points and midpoint, defaults to 15
        (optional)
        :param t: t is the thickness of the line drawn between the two points (p1 and p2) in the frame.
        It is set to 3 by default, defaults to 3 (optional)
        :return: a tuple with three elements: the distance between two points (length), the frame with
        the drawn lines and circles, and a list with the coordinates of the two points and the midpoint
        between them.
        """
        x1, y1 = self.lista[p1][1:]
        x2, y2 = self.lista[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if dibujar:
            cv2.line(frame, (x1,y1), (x2,y2), (0,0,255),t)
            cv2.circle(frame, (x1,y1), r, (0,0,255), cv2.FILLED)
            cv2.circle(frame, (x2,y2), r, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (cx,cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)

        return length, frame, [x1, y1, x2, y2, cx, cy]


def main():
    ptiempo = 0
    ctiempo = 0


    cap = cv2.VideoCapture(0)

    detector = detectormanos()

# The code is capturing video frames from the default camera using OpenCV's `VideoCapture` function.
# It then passes each frame to an instance of the `detectormanos` class to detect and track hands in
# the frame. The detected hand landmarks and connections are drawn on the frame using the
# `encontrarmanos` method of the `detectormanos` class. The `encontrarposicion` method is then used to
# find the position of the hand in the frame and draw a bounding box around it. The frame is then
# displayed using OpenCV's `imshow` function. The loop continues until the user presses the 'Esc' key,
# at which point the video capture is released and all windows are closed.
    while True:
        ret, frame = cap.read()
        frame = detector.encontrarmanos(frame)
        lista, bbox = detector.encontrarposicion(frame)

        ctiempo = time.time()
        fps = 1 / (ctiempo - ptiempo)
        ptiempo = ctiempo

        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Manos", frame)
        k = cv2.waitKey(1)

        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":
    main()