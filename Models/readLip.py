#---------Import Libraries-----------
import math
import time
import threading
import cv2
import dlib
import imutils
from PyQt5.QtGui import QImage, QPixmap
import os
from Helper import Logger

"""Import from another class"""


class Cam():
    def __init__(self, parent):
        self.stream = cv2.VideoCapture(0)
        self.parent = parent

        self.mouth_open_timer = time.time()

        global logger
        logger = Logger.Log()
        logger.info("Camera is working!")

        # ---------record video------------#
        # Get the default camera's properties
        fps = int(self.stream.get(cv2.CAP_PROP_FPS))
        width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

        output_directory = 'Outputs'
        # Define the codec and create VideoWriter object
        # For MOV format, you can use different codecs like 'mp4v', 'avc1', 'XVID', etc.
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' codec for MOV format
        self.output = cv2.VideoWriter(os.path.join(output_directory, 'temp_video.mov'), fourcc, fps, (width, height))

    def open_camera(self):

        detector = dlib.get_frontal_face_detector()

        # Load the predictor
        predictor = dlib.shape_predictor("../model/face_weights.dat")

        # read the image
        #stream = cv2.VideoCapture(0)

        #counter for number of frames needed to calibrate the not-talking lip distance
        determining_lip_distance = 50

        #store the not-talking lip distances when averaging
        lip_distances = []

        #threshold for determing if user is talking or not talking
        LIP_DISTANCE_THRESHOLD = None

        while True:
            global audio_start
            #global test_audio_thread
            #test_audio_thread = audio_record.AudioRecorder()
            ret, frame = self.stream.read()
            if not ret:
                break

            self.output.write(frame)
            #self.output = cv2.VideoWriter(self.video_filename, cv2.VideoWriter_fourcc(*'MJPG'), self.fps,
            #                              self.frameSize)

            gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)

            faces = detector(gray)

            for face in faces:
                x1, y1 = face.left(), face.top() # left point and top point
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

                    RED = (0, 0, 255)  # Not talking
                    YELLOW = (0, 255, 255) # Mouth is close

                    if lip_distance > LIP_DISTANCE_THRESHOLD:  # person is talking
                        cv2.putText(frame, "Talking", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                        #print("started to listen")
                        # global audio_thread
                        # audio_thread = audio_record.AudioRecorder()
                        #audio_thread.start()
                        #audio_start = audio_record.AudioRecorder()
                        #audio_start.record()

                        self.mouth_open_timer = time.time()
                        # print("started to listen")
                        # audio_thread = audio_record.AudioRecorder()
                        # audio_thread.start()
                        # time.sleep(5)
                        # audio_thread.stop()

                        #cv2.putText(frame, "RECORDING WORD RIGHT NOW", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, ORANGE, 2)

                    else:
                        if time.time() - self.mouth_open_timer > 5:
                            cv2.putText(frame, "Not talking", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, RED, 2)
                            #test_audio_thread.stop()
                            #audio_start.stop()
                        else:
                            cv2.putText(frame, "Mouth closed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, YELLOW, 2)
                        #cv2.putText(frame, "Not talking", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, RED, 2)

                else: #we are calibrating the not-talking distance
                    cv2.putText(frame, "KEEP MOUTH CLOSED, CALIBRATING DISTANCE BETWEEN LIPS", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    determining_lip_distance -= 1
                    distance = landmarks.part(58).y - landmarks.part(50).y
                    cv2.putText(frame, "Current distance: " + str(distance + 2), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                    lip_distances.append(distance)
                    if(determining_lip_distance == 0):
                        LIP_DISTANCE_THRESHOLD = sum(lip_distances) / len(lip_distances) + 2

            cv2.putText(frame, "Press 'ESC' ", (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) #to exit

            self.set_video(frame)

            #frame_show = cv2.resize(frame, (width, height))
            self.output.write(frame)
            #cv2.imshow(winname="Lip Reader", mat=frame_show) #this is for open the frame cam

            # for ESC keyword is 27 - here is option
            if cv2.waitKey(delay=1) == 27:
                break

        return self.stream

    def stop(self):
        try:
            self.output.release()
            self.stream.release()

            # Close all windows
            cv2.destroyAllWindows()
        except:
            print("No opened camera.")

    def set_video(self, frame):
        self.tmp = frame
        frame = imutils.resize(frame, width=900)
        frame_show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = QImage(frame_show, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.parent.imgLabel.setPixmap(QPixmap.fromImage(frame))

    def start(self):
        video_thread = threading.Thread(target=self.open_camera)
        video_thread.start()