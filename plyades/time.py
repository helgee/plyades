import datetime
import numpy as np

def datetime2jd(dt):
    return (367.0 * dt.year
            - np.floor((7 * (dt.year + np.floor((dt.month + 9) / 12.0))) * 0.25)
            + np.floor(275 * dt.month / 9.0)
            + dt.day + 1721013.5
            + ((dt.second / 60.0 + dt.minute) / 60.0 + dt.hour) / 24.0)
