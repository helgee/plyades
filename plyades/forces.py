import numpy as np

def newton(f, t, y, params):
    r = np.linalg.norm(y[:3])
    f[:3] += y[3:]
    f[3:] += -params['body'].mu*y[:3]/r**3

def newton_j2(f, t, y, params):
    r = np.sqrt(np.square(y[:3]).sum())
    mu = params['body'].mu.value
    j2 = params['body'].j2
    r_m = params['body'].mean_radius.value
    rx, ry, rz = y[:3]
    f[:3] += y[3:]
    pj = -3/2*mu*j2*r_m**2/r**5
    f[3] += -mu*rx/r**3 + pj*rx*(1-5*rz**2/r**2)
    f[4] += -mu*ry/r**3 + pj*ry*(1-5*rz**2/r**2)
    f[5] += -mu*rz/r**3 + pj*rz*(3-5*rz**2/r**2)
