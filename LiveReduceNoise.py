#!/usr/bin/python  

import pyaudio
import subprocess
import wave
import noisereduce as nr
import numpy as np

class Reduction_Noise():
    def start_reducing(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "audioNew.wav"

        p = pyaudio.PyAudio()

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
            reduced_noise = nr.reduce_noise(y=np_data, sr=RATE, thresh_n_mult_nonstationary=2, stationary=False)
            frames.append(reduced_noise.tobytes())

        print("Done!")

        microphone.stop_stream()
        microphone.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

a = Reduction_Noise()
a.start_reducing()
"""
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "audio.wav"

p = pyaudio.PyAudio()

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
    reduced_noise = nr.reduce_noise(y=np_data, sr=RATE, thresh_n_mult_nonstationary=2, stationary=False)
    frames.append(reduced_noise.tobytes())



print("Done!")

microphone.stop_stream()
microphone.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
#player = subprocess.Popen(["aplay", WAVE_OUTPUT_FILENAME])
"""