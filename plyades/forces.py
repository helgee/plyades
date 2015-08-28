import numpy as np

def newton(s):
    f = np.zeros(6)
    r = np.linalg.norm(s.r.value)
    f[:3] += s.v.value
    f[3:] += -s.body.mu*s.r.value/r**3
    return f
