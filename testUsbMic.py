import pyaudio
import subprocess
import wave
import noisereduce as nr
import numpy as np
import cv2


class Reduction_Noise():
    def start_reducing(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        RATE = 44100
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "audioNew.wav"

        p = pyaudio.PyAudio()

        # Get default input device info
        default_device_info = p.get_default_input_device_info()
        CHANNELS = default_device_info['maxInputChannels']

        microphone = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

        print("Recording...")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = microphone.read(CHUNK)
            np_data = np.frombuffer(data, dtype=np.int16)

            # Convert stereo to mono if necessary
            if CHANNELS == 2:
                np_data = np.mean(np_data.reshape(-1, 2), axis=1).astype(np.int16)

            reduced_noise = nr.reduce_noise(y=np_data, sr=RATE,
                                            thresh_n_mult_nonstationary=2, stationary=False)
            frames.append(reduced_noise.tobytes())

        print("Done!")

        microphone.stop_stream()
        microphone.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(1)  # Set channels to 1 for mono output
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


# Instantiate the class and call the method
#reducer = Reduction_Noise()
#reducer.start_reducing()
