import speech_recognition as sr
import threading
from Helper import Logger

class TransfromSpeechToText():
    def __init__(self, parent):
        self.parent = parent

        global logger
        logger = Logger.Log()

    def test(self, text):
        print("You said:", text)
        self.parent.label.setText(text)
        #logger.info("Subtitle:" + text)

    def recognize_audio_file(self, audio_file):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        return audio_data

    def speech_to_text(self, audio_data):
        recognizer = sr.Recognizer()
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            logger.info("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None

    def start_to_listen(self, audio_file):
        audio_data = self.recognize_audio_file(audio_file)
        text = self.speech_to_text(audio_data)
        if text:
            self.test(text)

    def start(self):
        audio_file_path = "Outputs/temp_audio.wav"
        sub_thread = threading.Thread(target=self.start_to_listen, args=(audio_file_path,))
        sub_thread.start()

# if __name__ == "__main__":
#     # Kullanmak istediğiniz ses dosyasının yolunu belirtin
#     audio_file_path = "temp_audio.wav"
#
#     # transfrom_speech_to_text sınıfından bir örnek oluşturun
#     instance = TransfromSpeechToText()
#
#     # Ses dosyasını işlemek için başlatın
#     instance.start(audio_file_path)
