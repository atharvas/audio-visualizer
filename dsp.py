import numpy as np
import scipy.fft
from scipy import signal
from config import *
from melmat import *

class DSP:
    def __init__(self, ALPHA_SMOOTHING):
        self.old_sample = None
        self.order = 5
        self.cutoff_freq = 2000 # 2KHz
        self.cuttoff_frac = self.cutoff_freq / (0.5 * RATE) 
        self.b_h, self.a_h = signal.butter(N=self.order, Wn=self.cuttoff_frac, btype='high', fs=RATE)
        self.melmat = get_mel_filtermatrix(n_filters=N_MEL_FILT, size=FFT_SIZE, low_hz=LOW, high_hz=HIGH, sampling_rate=RATE)

    def process_sample(self, raw_sample):
        # print(len(raw_sample))
        filtered_sig = raw_sample # signal.filtfilt(self.b_h, self.a_h, raw_sample)
        correted_sig = filtered_sig * np.hamming(len(filtered_sig))
        fft_output = np.abs(np.fft.rfft(correted_sig))
        pwr_spectrum = (1/ len(fft_output)) * (fft_output)**2
        output = self.log_bins(pwr_spectrum) 
        # For mel matrix output use:
        # output = 20 * np.log10(self.melmat @ pwr_spectrum)
        # Exponential Smoothing Filter.
        if self.old_sample is not None:
            smoothed_output = ALPHA_SMOOTHING * output + (1 - ALPHA_SMOOTHING) * self.old_sample
            self.old_sample = smoothed_output
        else:
            self.old_sample = output
            smoothed_output = ALPHA_SMOOTHING * output + (1 - ALPHA_SMOOTHING) * self.old_sample

        return smoothed_output

    def log_bins(self, sample):
        log_space = 2**np.arange(np.log2(len(sample)))
        indices   = [int(np.sqrt(log_space[i - 1] * log_space[i])) for i in range(1, len(log_space))]
        bins      = np.array([np.mean(lbin) for lbin in np.split(sample, indices)])
        return bins