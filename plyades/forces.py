import numpy as np

def newton(f, t, y, params):
    r = np.linalg.norm(y[:3])
    f[:3] += y[3:]
    f[3:] += -params['body'].mu*y[:3]/r**3
