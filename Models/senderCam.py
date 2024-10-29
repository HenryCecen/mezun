# Welcome to PyShine

# This code is for the server
# Lets import the libraries
import socket, cv2, pickle, struct, imutils
from Helper import Logger
import dlib
import math
from PyQt5.QtGui import QImage, QPixmap


class Streaming():
    def __init__(self, parent):
        self.parent = parent

        global logger
        logger = Logger.Log()

    def open_stream(self):
        # Socket Create
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print('HOST IP:', host_ip)
        log_host = "HOST IP: " + host_ip
        logger.info(log_host)
        port = 9999
        socket_address = (host_ip, port)

        # Socket Bind
        server_socket.bind(socket_address)

        # Socket Listen
        server_socket.listen(5)
        print("LISTENING AT:", socket_address)

        detector = dlib.get_frontal_face_detector()

        # Load the predictor
        predictor = dlib.shape_predictor("../model/face_weights.dat")

        # Socket Accept
        while True:
            self.client_socket, addr = server_socket.accept()
            print('GOT CONNECTION FROM:', addr)
            if self.client_socket:

                vid = cv2.VideoCapture(0)

                # counter for number of frames needed to calibrate the not-talking lip distance
                determining_lip_distance = 50

                # store the not-talking lip distances when averaging
                lip_distances = []

                # threshold for determing if user is talking or not talking
                LIP_DISTANCE_THRESHOLD = None

                while (vid.isOpened()):
                    _, frame = vid.read()

                    # ---------------------------------------------------------------------------#
                    gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)

                    faces = detector(gray)

                    for face in faces:
                        x1, y1 = face.left(), face.top()  # left point and top point
                        x2, y2 = face.right(), face.bottom()  # right point and bottom point

                        # Create landmark object
                        landmarks = predictor(image=gray, box=face)

                        # Calculate the distance between the upper and lower lip landmarks
                        mouth_top = (landmarks.part(51).x, landmarks.part(51).y)
                        mouth_bottom = (landmarks.part(57).x, landmarks.part(57).y)
                        lip_distance = math.hypot(mouth_bottom[0] - mouth_top[0], mouth_bottom[1] - mouth_top[1])

                        # lip landmarks
                        lip_left = landmarks.part(49).x  # origin 48
                        lip_right = landmarks.part(55).x  # origin 54
                        lip_top = landmarks.part(51).y  # origin 50
                        lip_bottom = landmarks.part(58).y

                        # if user enters custom lip distance or script finishes calibrating
                        if (determining_lip_distance != 0 and LIP_DISTANCE_THRESHOLD != None):

                            # Draw a circle around the mouth
                            for n in range(48, 61):
                                x = landmarks.part(n).x
                                y = landmarks.part(n).y
                                cv2.circle(img=frame, center=(x, y), radius=3, color=(0, 255, 0), thickness=-1)

                            ORANGE = (0, 180, 255)  # RECORDING WORD RIGHT NOW
                            BLUE = (255, 0, 0)  # NOT RECORDING WORD
                            RED = (0, 0, 255)  # Not talking

                            # print(len(curr_word_frames))

                            if lip_distance > LIP_DISTANCE_THRESHOLD:  # person is talking
                                cv2.putText(frame, "Talking", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                                # cv2.putText(frame, "RECORDING WORD RIGHT NOW", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, ORANGE, 2)
                            elif lip_distance == LIP_DISTANCE_THRESHOLD:
                                cv2.putText(frame, "Could not find Mouth!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                            (0, 255, 0),
                                            2)

                            else:
                                cv2.putText(frame, "Not talking", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, RED, 2)

                        else:  # we are calibrating the not-talking distance
                            cv2.putText(frame, "KEEP MOUTH CLOSED, CALIBRATING DISTANCE BETWEEN LIPS", (50, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                            determining_lip_distance -= 1
                            distance = landmarks.part(58).y - landmarks.part(50).y
                            cv2.putText(frame, "Current distance: " + str(distance + 2), (50, 100),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (255, 255, 255), 2)

                            lip_distances.append(distance)
                            if (determining_lip_distance == 0):
                                LIP_DISTANCE_THRESHOLD = sum(lip_distances) / len(lip_distances) + 2

                    cv2.putText(frame, "Press 'ESC' to exit", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
                                2)
                    # ---------------------------------------------------------------------------#

                    # frame = imutils.resize(frame, width=900)
                    # a = pickle.dumps(frame)
                    # message = struct.pack("Q", len(a)) + a
                    # self.client_socket.sendall(message)
                    self.set_to_video(frame)

                    #cv2.imshow('TRANSMITTING VIDEO', frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        self.client_socket.close()

    #############TEST EDİLECEK BURASI
    def set_to_video(self, frame):
        self.tmp = frame
        frame2 = imutils.resize(frame, width=900)
        a = pickle.dumps(frame2)
        message = struct.pack("Q", len(a)) + a
        self.client_socket.sendall(message)
        #cv2.imshow('TRANSMITTING VIDEO', frame2)
        frame_show = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        frame3 = QImage(frame_show, frame2.shape[1], frame2.shape[0], frame2.strides[0], QImage.Format_RGB888)
        self.parent.imgLabel.setPixmap(QPixmap.fromImage(frame3))