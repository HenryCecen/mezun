import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (bytes per sample)
CHANNELS = 1  # Single channel for microphone input
RATE = 44100  # Sample rate (samples per second)
WINDOW_SIZE = 512
OVERLAP = 256

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Initialize plot
fig, ax = plt.subplots()
extent = (0, CHUNK/RATE, 0, RATE/2)
img = ax.imshow(np.zeros((WINDOW_SIZE//2 + 1, CHUNK//OVERLAP)),
                aspect='auto',
                origin='lower',
                extent=extent
                )
'''
x = np.arange(0, 2 * CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK))


# Formatting for the plot
ax.set_ylim(0, 255)
ax.set_xlim(0, CHUNK)
'''

# Function to update plot
def update_plot(frame):
    data = np.frombuffer(stream. read(CHUNK), dtype=np.int16)
    spec, _, _ = plt.mlab.specgram(data, NFFT=WINDOW_SIZE, Fs=RATE, noverlap=OVERLAP)
    #line.set_ydata(data) #line yerine img
    img.set_array(spec)
    return img,

# Run animation
ani = FuncAnimation(fig, update_plot, blit=True)
plt.show()

# Close stream
stream.stop_stream()
stream.close()
p.terminate()
