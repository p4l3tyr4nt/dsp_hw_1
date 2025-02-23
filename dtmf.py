import numpy as np
import pandas as pd
import plotly.express as px

freq_array_1 = np.array([1209, 1336, 1477])
freq_array_2 = np.array([697, 770, 852, 941])

freq_matrix = np.linspace(1, 9, num=9, dtype=int).reshape(3, 3)

class Signal:
    def __init__(self, num: str, x: np.ndarray, t: np.ndarray, part: float):
        self.num = num
        self.x = x
        self.t = t
        self.last = int(len(x) * part)
    
    def get_graph(self):
        df = pd.DataFrame({'Signal': self.x[:self.last], 't': self.t[:self.last]})
        return px.line(df, x='t', y='Signal', title=f'Signal for {self.num}')

def get_signal(num: str, sample_rate_kHz: int, duration: float, part: float) -> Signal:
    
    t = np.linspace(0, duration, num=round(duration * sample_rate_kHz * 1e3))

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

    return Signal(num, x, t, part)