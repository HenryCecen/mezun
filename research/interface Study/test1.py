
"""
import os
import sys
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
import cv2
import numpy as np

class MyApp(QDialog):
    image_data = pyqtSignal(QImage)

    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        uic.loadUi(os.path.join("C:/Users/ASUS/PycharmProjects/mezun/interface.ui"), self)

        self.btnOpenCamera.clicked.connect(self.open_camera)

        self.image_data.connect(self.update_image_label)

        self.camera = cv2.VideoCapture(0)  # Assuming camera index 0

    def update_image_label(self, image):
        self.imgLabel.setPixmap(QPixmap.fromImage(image))

    def open_camera(self):
        print("works")
        while True:
            ret, frame = self.camera.read()
            if not ret:
                break

            # Convert frame to RGB
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Resize the frame to match the label size
            resized_image = cv2.resize(rgb_image, (self.imgLabel.width(), self.imgLabel.height()))

            # Convert the frame to QImage
            h, w, ch = resized_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(resized_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Emit the signal to update the label with the new frame
            self.image_data.emit(qt_image)

            # Display the frame in a window (optional)
            cv2.imshow("Camera", frame)
            if cv2.waitKey(1) == ord('q'):
                break

        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

"""
import os
import sys
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QTimer
import cv2


class MyApp(QDialog):
    image_data = pyqtSignal(QImage)

    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        uic.loadUi(os.path.join("/view/interface.ui"), self)

        self.btnOpenCamera.clicked.connect(self.open_camera)

        self.image_data.connect(self.update_image_label)

        self.camera = cv2.VideoCapture(0)  # Assuming camera index 0

        # Create a timer to update the camera feed regularly
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera)

    def update_image_label(self, image):
        self.imgLabel.setPixmap(QPixmap.fromImage(image))

    def open_camera(self):
        print("Camera opened")
        # Start the timer to update the camera feed
        self.timer.start(30)  # Update every 30 milliseconds

    def update_camera(self):
        ret, frame = self.camera.read()
        if not ret:
            return

        # Convert frame to RGB
        interface_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Resize the frame to match the label size
        resized_image = cv2.resize(interface_frame, (self.imgLabel.width(), self.imgLabel.height()))

        # Convert the frame to QImage
        h, w, ch = resized_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(resized_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Emit the signal to update the label with the new frame
        self.image_data.emit(qt_image)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
