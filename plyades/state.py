from __future__ import division
from __future__ import print_function
import numpy as np
import util
from time import Epoch


class State:
    def __init__(self, s, epoch=Epoch(2000, 1, 1, 0, 0, 0), frame="MEE2000"):
        self.s = s
        self.r = s[0:3]
        self.v = s[3:6]
        self.t = epoch
        self.frame = frame

    def __str__(self):
        out = ["Time (UT1): {}",
               "Julian date (MJD2000): {}",
               "Reference Frame: {}",
               "x [km]: {}",
               "y [km]: {}",
               "z [km]: {}",
               "vx [km]: {}",
               "vy [km]: {}",
               "vz [km]: {}"]
        return ("\n".join(out).format(self.t, self.t.jd2000, self.frame, *self.s))


def precession(date):
    ''' Vallado 2nd p.215
    '''
    # Julian centuries since the epoch
    t = (date - 2451545)/36525
    zeta = util.dms2rad(0, 0, 2306.2181*t + 0.30188*t**2 + 0.017998*t**3)
    theta = util.dms2rad(0, 0, 2004.3109*t - 0.42665*t**2 - 0.041833*t**3)
    z = util.dms2rad(0, 0, 2306.2181*t + 1.09468*t**2 + 0.018203*t**3)
    # Determine rotational matrices.
    M1 = util.rot(-z, axis=3)
    M2 = util.rot(theta, axis=2)
    M3 = util.rot(-zeta, axis=3)
    return np.dot(M1, np.dot(M2, M3))
