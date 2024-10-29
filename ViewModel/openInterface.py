import os
import time

from PyQt5.QtGui import QImage, QIcon
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from Models import audio_record, readLip, senderCam, transfromer
from Helper import message, Logger, merger


class MyApp(QDialog):
    image_data = pyqtSignal(QImage)

    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        uic.loadUi(os.path.join("../view/interface.ui"), self)

        self.setWindowIcon(
            QIcon('C:/Users/ASUS/PycharmProjects/mezun/helper/icon-logo.jpg'))  # Specify the path to your icon file

        self.btnStop.setDisabled(True)
        self.buttons()

        # Write the logger
        global logger
        logger = Logger.Log()

    def buttons(self):
        self.btnOpenCamera.clicked.connect(self.display_camera)  # Opening cam
        self.btnStream.clicked.connect(self.show_stream_cam)  # Opening socket cam
        self.btnStop.clicked.connect(self.stop_all_cam)  # Close all cam and mic

    def show_stream_cam(self):
        self.btnOpenCamera.setDisabled(True)
        self.btnStop.setEnabled(True)
        stream = senderCam.Streaming(self)
        stream.open_stream()

    def display_camera(self, parent):
        logger.info("The interface is working")
        if self.label == None:
            self.label.clear()
        message.message_ok()
        self.btnStream.setDisabled(True)
        self.btnStop.setEnabled(True)
        self.btnOpenCamera.setDisabled(True)

        global audio_thread
        global display_thread

        # camera = readLip.Cam(self)
        # video_thread = threading.Thread(target=camera.open_camera)
        display_thread = readLip.Cam(self)
        display_thread.start()

        audio_thread = audio_record.AudioRecorder()
        audio_thread.start()

    def stop_all_cam(self):
        message.message_close()
        logger.info("Cam and microphone are clossed")
        print("Stopped the audio")
        audio_thread.stop()  # Close the microphone

        print("Stopped the video")
        display_thread.stop()  # Close the camera
        self.imgLabel.clear()

        # ---------Here will be transformed speech to text in the label of the GUI----------------#
        transformer = transfromer.TransfromSpeechToText(self)
        transformer.start()

        time.sleep(5)
        # ---------After recording video and audio, we can merge these two------------------------#
        merger_movie = merger.MergerMovie()
        merger_movie.merge()

        # -------fix buttons----------#
        self.btnStop.setDisabled(True)
        self.btnStream.setEnabled(True)
        self.btnOpenCamera.setEnabled(True)

# def Start_Application():
#     app = QApplication(sys.argv)
#     window = MyApp()
#     window.show()
#     sys.exit(app.exec_())
#
# if __name__ == "__main__":
#     Start_Application()
