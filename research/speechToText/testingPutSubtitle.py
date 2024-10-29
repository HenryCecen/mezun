import speech_recognition as sr
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

class transfrom_speech_to_text():
    def __init__(self, parent):
        self.parent = parent

    def test(self, text):
        #Here text will be put in label in GUI
        self.parent.label.setText(text)
        #self.parent.textBrowser.setText(text) #bu çalışmadı kesin

    def listen_microphone(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio_data = recognizer.listen(source)
        return audio_data

    def test2(self):
        # Create a Recognizer instance
        recognizer = sr.Recognizer()

        # Capture audio input from the microphone
        with sr.Microphone() as source:
            print("Speak something...")
            audio_data = recognizer.listen(source)

        # Perform speech recognition using Google Web Speech API
        try:
            text = recognizer.recognize_google(audio_data)
            print("You said:", text)
            self.test(text)
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print("Error: Could not request results from Google Speech Recognition service;")
    def speech_to_text(self, audio_data):
        while True:
            recognizer = sr.Recognizer()
            try:
                text = recognizer.recognize_google(audio_data)
                return text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def start_to_listen(self):
        audio_data = self.listen_microphone()
        text = self.speech_to_text(audio_data)
        if text:
            # openInterface.graphicsView.addText(text)
            print("You said:", text)
            #self.parent.label.setText(text)
            #self.test(text)

            #class_frame = readLip.Cam(self)
            #for_frame = class_frame.open_camera()
            #readLip.cv2.putText(for_frame.frame, text, (50, 50), readLip.cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    def start(self):
        sub_thread = threading.Thread(target=self.test2)
        sub_thread.start()

# if __name__ == "__main__":
#     audio_data = listen_microphone()
#     text = speech_to_text(audio_data)
#     if text:
#         print("You said:", text)

# if __name__ == "__main__":
#     texttt = transfrom_speech_to_text(None)
#     texttt.start()

