import os
import numpy as np
import pandas as pd
import plotly.express as px
from scipy.io.wavfile import write

freq_array_1 = np.array([1209, 1336, 1477])
freq_array_2 = np.array([697, 770, 852, 941])

freq_matrix = np.linspace(1, 9, num=9, dtype=int).reshape(3, 3)

class Signal:
    def __init__(self, num: str, x: np.ndarray, t: np.ndarray):
        self.num = num
        self.x = x
        self.t = t
    
    def get_graph(self, part: float = 0.125):
        last = int(len(self.x) * part)
        df = pd.DataFrame({'Signal': self.x[:last], 't': self.t[:last]})
        return px.line(df, x='t', y='Signal', title=f'Signal for {self.num}')
    
    def generate_audio(self, sample_rate_kHz: int):
        amplitude = np.iinfo(np.int16).max
        audio_data = amplitude * self.x / np.max(self.x)
        if not os.path.exists('audio/'):
            os.makedir('audio/')
        write('audio/dtmf.wav', int(sample_rate_kHz * 1e3), audio_data.astype(np.int16))

def get_signal(num: str, sample_rate_kHz: int, duration: float = 1) -> Signal:

    t = np.linspace(0, duration, num=int(duration * sample_rate_kHz * 1e3))

    if num.isdigit():
        if num == '0':
            idx_1 = 1
            idx_2 = 3
        else:
            idx_1 = np.where(freq_matrix==int(num))[0][0]
            idx_2 = np.where(freq_matrix==int(num))[1][0]
    else:
        if num == '*':
            idx_1 = 0
            idx_2 = 3
        elif num == '#':
            idx_1 = 2
            idx_2 = 3
        else:
            idx_1 = None
            idx_2 = None

    freq_1 = freq_array_1[idx_1]
    freq_2 = freq_array_2[idx_2]

    x = np.sin(2 * np.pi * freq_1 * t) + np.sin(2 * np.pi * freq_2 * t)

    return Signal(num, x, t)