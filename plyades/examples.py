import numpy as np
from plyades.core import State
from plyades.bodies import EARTH
from astropy.time import Time
import astropy.units as u

iss_r = np.array([
    8.59072560e+02,
    -4.13720368e+03,
    5.29556871e+03,
])*u.km
iss_v = np.array([
    7.37289205e+00,
    2.08223573e+00,
    4.39999794e-01,
])*u.km/u.s
iss_t = Time("2013-03-18T12:00:00.000")
iss = State(iss_r, iss_v, iss_t)
