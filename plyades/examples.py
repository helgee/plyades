from __future__ import division
import datetime
import numpy as np
from plyades.core import State, Orbit

iss_state = np.array([
    8.59072560e+02,
    -4.13720368e+03,
    5.29556871e+03,
    7.37289205e+00,
    2.08223573e+00,
    4.39999794e-01,
    ])
iss_epoch = datetime.datetime(2013, 3, 18, 12, 0)
iss = State(iss_state, t=iss_epoch, body="Earth", frame="MEE2000")

