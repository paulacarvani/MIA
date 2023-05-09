import cv2
import mediapipe as mp
import numpy as np
from math import acos, degrees
import random


def palm_centroid(coordinates_list):
    """
    The function takes a list of coordinates and returns the centroid as a tuple of integers.

    :param coordinates_list: The input parameter "coordinates_list" is a list of tuples, where each
    tuple represents the (x,y) coordinates of a point in a 2D space. This function calculates the
    centroid of all the points in the list and returns it as a tuple of integers representing the (x,y)
    coordinates
    :return: The function `palm_centroid` returns the centroid of a list of coordinates as a tuple of
    integers.
    """
    coordinates = np.array(coordinates_list)
    centroid = np.mean(coordinates, axis=0)
    centroid = int(centroid[0]), int(centroid[1])
    return centroid


def fingers_up_down(hand_results, thumb_points, palm_points, fingertips_points, finger_base_points):
    """
    The function extracts the coordinates of various points on the hand landmarks, including the thumb,
    palm, fingertips, and finger bases.

    :param hand_results: The output of the hand detection model, which contains information about the
    location and landmarks of the detected hand(s)
    :param thumb_points: A list of integers representing the indices of the landmarks corresponding to
    the thumb in the hand landmarks array
    :param palm_points: A list of landmark indices corresponding to the points on the palm of the hand
    :param fingertips_points: A list of landmark indices corresponding to the fingertips of each finger
    (excluding the thumb) in the hand landmarks
    :param finger_base_points: A list of landmark indices representing the base of each finger
    (excluding the thumb) in the hand landmarks
    """
    fingers = None
    coordinates_thumb = []
    coordinates_palm = []
    coordinates_ft = []
    coordinates_fb = []
    for hand_landmarks in hand_results.multi_hand_landmarks:
        for index in thumb_points:
            x = int(hand_landmarks.landmark[index].x * width)
            y = int(hand_landmarks.landmark[index].y * height)
            coordinates_thumb.append([x, y])

        for index in palm_points:
            x = int(hand_landmarks.landmark[index].x * width)
            y = int(hand_landmarks.landmark[index].y * height)
            coordinates_palm.append([x, y])

        for index in fingertips_points:
            x = int(hand_landmarks.landmark[index].x * width)
            y = int(hand_landmarks.landmark[index].y * height)
            coordinates_ft.append([x, y])

        for index in finger_base_points:
            x = int(hand_landmarks.landmark[index].x * width)
            y = int(hand_landmarks.landmark[index].y * height)
            coordinates_fb.append([x, y])

        # Thumb
        """This code is calculating the lengths of the sides of a triangle formed by three points in the
        # `coordinates_thumb` list. The three points are represented as numpy arrays `p1`, `p2`, and `p3`, and
        # the lengths of the sides are calculated using the `np.linalg.norm()` function. These lengths are
        # stored in variables `l1`, `l2`, and `l3`.
        """
        p1 = np.array(coordinates_thumb[0])
        p2 = np.array(coordinates_thumb[1])
        p3 = np.array(coordinates_thumb[2])

        l1 = np.linalg.norm(p2 - p3)
        l2 = np.linalg.norm(p1 - p3)
        l3 = np.linalg.norm(p1 - p2)

        # Angle
        """This code calculates the angle between the thumb and the index finger based on the lengths
        of the sides of a triangle formed by three points in the `coordinates_thumb` list. The three
        points are represented as numpy arrays `p1`, `p2`, and `p3`, and the lengths of the sides
        are calculated using the `np.linalg.norm()` function. The variable `to_angle` is then
        calculated using the law of cosines, and the angle between the thumb and index finger is
        calculated using the `acos()` and `degrees()` functions. If the value of `to_angle` is -1
        (which can happen due to floating point errors), the angle is set to 180 degrees. Finally,
        if the angle is greater than 150 degrees, the variable `thumb_finger` is set to `True`."""
        to_angle = (l1**2 + l3**2 - l2**2) / (2 * l1 * l3)
        if int(to_angle) == -1:
            angle = 180
        else:
            angle = degrees(acos(to_angle))
        thumb_finger = np.array(False)
        if angle > 150:
            thumb_finger = np.array(True)

        # Other fingers
        """This code is calculating the centroid of the palm landmarks by calling the `palm_centroid()`
        function and passing in the `coordinates_palm` list as an argument. The function returns the
        centroid as a tuple of integers, which are then unpacked into the variables `nx` and `ny`."""
        nx, ny = palm_centroid(coordinates_palm)
        cv2.circle(frame, (nx, ny), 3, (0, 255, 0), 2)
        coordinates_centroid = np.array([nx, ny])
        coordinates_ft = np.array(coordinates_ft)
        coordinates_fb = np.array(coordinates_fb)

        # Distances
        """This code is calculating the distances between the centroid of the palm landmarks and the fingertips
        and finger bases of each finger (excluding the thumb). It first calculates the Euclidean distance
        between the centroid and each fingertip and finger base using the `np.linalg.norm()` function. It
        then subtracts the distance between the centroid and each finger base from the distance between the
        centroid and each fingertip to get the difference between the two distances. If the difference is
        greater than 0, it means that the fingertip is farther away from the centroid than the finger base,
        indicating that the finger is extended. The results are stored in a boolean array `fingers`. The
        code then appends the `thumb_finger` variable (which indicates whether the thumb is extended or not)
        to the `fingers` array using the `np.append()` function. Finally, the code uses the
        `mp_drawing.draw_landmarks()` function to draw the hand landmarks and connections on the input
        `frame`."""
        d_centrid_ft = np.linalo.norm(
            coordinates_centroid - coordinates_ft, axis=1)
        d_centrid_fb = np.linalo.norm(
            coordinates_centroid - coordinates_fb, axis=1)
        dif = d_centrid_ft - d_centrid_fb
        fingers = dif > 0
        fingers = np.append(thumb_finger, fingers)

        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style()
        )
    return fingers


# The code initializes various variables and constants used in the rock-paper-scissors game.
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

thumb_points = [1, 2, 4]
palm_points = [0, 1, 2, 9, 13, 17]
fingertips_points = [8, 12, 16, 20]
finger_base_points = [6, 10, 14, 18]

TO_ACTIVATE = np.array([True, False, False, False, False])
PIEDRA = np.array([False, False, False, False, False])
PAPEL = np.array([True, True, True, True, True])
TIJERAS = np.array([False, True, True, False, False])

# Rules
WIN_GAME = ["02", "10", "21"]
pc_option = False
detect_hand = True

THRESHOLD = 10
THRESHOLD_RESTART = 50

count_like = 0
count_piedra = 0
count_papel = 0
count_tijeras = 0
count_restart = 0

# Images
image1 = cv2.imread("0.jpeg")
image2 = cv2.imread("1.jpeg")
image_winner = cv2.imread("V2.jpeg")
image_tie = cv2.imread("V3.jpeg")
image_loser = cv2.imread("V1.jpeg")

imAux = image1

player = None

with mp_hands.Hands(
    model_complexity=1,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
                fingers = fingers_up_down(results,
                                            thumb_points, palm_points, fingertips_points, finger_base_points)

                if detect_hand == True:
                    if not False in (fingers == TO_ACTIVATE) and pc_option == False:
                            if count_like >= THRESHOLD:
                                pc = random.randint(0, 2)
                                print("pc:", pc)
                                pc_option = True
                                imAux = image2
                            count_like += 1

                    if pc_option == True:
                            if not False in (fingers == PIEDRA):
                                if count_piedra >= THRESHOLD:
                                    player = 0
                                count_piedra += 1
                            elif not False in (fingers == PAPEL):
                                if count_papel >= THRESHOLD:
                                    player = 1
                                count_papel += 1
                            elif not False in (fingers == TIJERAS):
                                if count_tijeras >= THRESHOLD:
                                    player = 2
                                count_tijeras += 1
        if player is not None:
            detect_hand = False
            if pc == player:
                imAux = image_tie
            else:
                if (str(player) + str(pc)) in WIN_GAME:
                    imAux = image_winner
                else:
                    imAux = image_loser
            count_restart += 1
            if count_restart > THRESHOLD_RESTART:
                pc_option = False
                detect_hand = True
                player = None
                count_like = 0
                count_piedra = 0
                count_papel = 0
                count_tijeras = 0
                count_restart = 0
                imAux = image1

        n_image = cv2.hconcat([imAux, frame])
        cv2.imshow("n_image", n_image)
        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()
