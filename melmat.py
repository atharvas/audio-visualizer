import numpy as np

# implementation adapted from https://haythamfayek.com/2016/04/21/speech-processing-for-machine-learning.html
def hz_to_mel(hz):
    return 2595 * np.log10(1 + (hz / 2) / 700)

def mel_to_hz(mel):
    return 700 * (10**(mel / 2595) - 1)

def get_mel_filtermatrix(n_filters=24, size=512, low_hz=0, high_hz=16000, sampling_rate=44100):
    low_mel = hz_to_mel(low_hz)
    high_mel = hz_to_mel(high_hz)
    points_in_mel = np.linspace(low_mel, high_mel, n_filters + 2) 
    points_in_hz = mel_to_hz(points_in_mel)
    center_freq = np.floor((size + 1) * points_in_hz / sampling_rate).astype(int)

    freq_to_mel_matrix = np.zeros((n_filters, int(np.floor(size / 2 + 1))))

    for i in range(1, len(center_freq) - 1):
        low_f = int(center_freq[i - 1])
        center_f = int(center_freq[i])
        high_f = int(center_freq[i + 1])
        inc_slope_idx = np.arange(low_f, center_f) # +ve triangle filter slope
        dec_slope_idx = np.arange(center_f, high_f)
        freq_to_mel_matrix[i - 1, inc_slope_idx] = (inc_slope_idx - low_f) / (center_f - low_f)
        freq_to_mel_matrix[i - 1, dec_slope_idx] = (high_f - dec_slope_idx) / (high_f - center_f)

    return freq_to_mel_matrix


    