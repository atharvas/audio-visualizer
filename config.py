import pyaudio

# HIGH LEVEL VARIABLES
FORMAT                  = pyaudio.paInt16
CHANNELS                = 1
RATE                    = 44100             # check SCANNING DEVICES OUTPUT.
FPS                     = 40
FRAMES_PER_BUFFER       = int(RATE/FPS)     # 50ms 
DEVICE_ID               = 2                 # check SCANNING DEVICES OUTPUT.
FFT_SIZE                = FRAMES_PER_BUFFER
N_MEL_FILT              = 48
LOW                     = 0
HIGH                    = RATE
VISUALIZER_LENGTH       = 20
VISUALIZER_HEIGHT       = 10
ALPHA_SMOOTHING         = 0.3