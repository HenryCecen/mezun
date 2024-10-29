import time
import wave
import pyaudio
import threading
import numpy as np
import noisereduce as nr

class AudioRecorder():
    def __init__(self):
        self.open = True
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        self.audio_filename = "C:/Users/ASUS/PycharmProjects/mezun/ViewModel/Outputs/temp_audio.wav"
        self.audio = pyaudio.PyAudio()

        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        self.audio_frames = []

    def record(self):
        self.stream.start_stream()
        while (self.open == True):
            data = self.stream.read(self.frames_per_buffer)
            np_data = np.frombuffer(data, dtype=np.int16)

            reduced_noise = nr.reduce_noise(y=np_data, sr=self.rate, thresh_n_mult_nonstationary=4, stationary=False)
            #updated_data = reduced_noise * 5
            self.audio_frames.append(reduced_noise)  # data olarak reduce_noise koydum

            # audio_data_bytes = reduced_noise.tobytes()
            # with sr.Microphone() as source:
            #     audio_data = self.r.record(source)
            #
            # recognized_text = self.r.recognize_google(audio_data, language='en-UK')
            # print("Text: " + recognized_text)
            # if self.open == False:
            #     break

    def stop(self):
        if self.open == True:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

            waveFile = wave.open(self.audio_filename, 'wb')
            waveFile.setnchannels(self.channels)  # Set channels to 1 for mono output
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()

            print("Clossed the microphone.")
        pass

    def start(self):
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()
        print("Started to record the wav file.")

if __name__ == "__main__":
# # Burası çalıştığı main kaldırıldı
    print("Started")
    starting_audio = AudioRecorder()
    starting_audio.start()
    time.sleep(8)
    starting_audio.stop()
    print("Done")