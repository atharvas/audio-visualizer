import pyaudio
import numpy as np
from scipy import signal
from microphone import Microphone
from melmat import *
from dsp import DSP
from config import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

ax.set_xlim([0,VISUALIZER_LENGTH])
ax.set_ylim([0,VISUALIZER_HEIGHT])

x_axis = np.arange(VISUALIZER_LENGTH)
y_axis = np.zeros(VISUALIZER_LENGTH)

line, = ax.plot(x_axis, y_axis)

mic = Microphone(FORMAT=FORMAT, CHANNELS=CHANNELS, RATE=RATE, FRAMES_PER_BUFFER=FRAMES_PER_BUFFER, DEVICE_ID=DEVICE_ID)
sig_processor = DSP(ALPHA_SMOOTHING=ALPHA_SMOOTHING)
def init():  # only required for blitting to give a clean slate.
    x_data = np.arange(VISUALIZER_LENGTH)
    y_data = np.zeros(len(x_data))
    line.set_data(x_data, y_data)
    return line,

def animate(i):
    x_data = np.arange(VISUALIZER_LENGTH)
    y_data = np.zeros(len(x_data))
    raw_data = mic.sampleInput()
    if sum(raw_data) > 0:
        processed_data = sig_processor.process_sample(raw_data)
        y_data =  np.concatenate((processed_data[::-1], processed_data))
        y_data = y_data / y_data.mean() 
        x_data =  np.arange(len(y_data))
    line.set_data(x_data, y_data)
    return line,


ani = animation.FuncAnimation(
    fig, animate, blit=True,
    init_func=init,
    frames = 10,
    interval=10
)

plt.show()

mic.destroy()