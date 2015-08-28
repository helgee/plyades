from astropy.table import Table
from astropy.time import TimeDelta
from bokeh.plotting import show
from bokeh.io import vplot
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

import plyades.kepler as kepler
import plyades.util as util
import plyades.visualization as vis

class Orbit:
    def __init__(
        self, s0, dt, epochs, states,
        elements=None, interpolate=False,
        **kwargs
    ):
        default_names = [
            'dt',
            'epoch',
            'rx',
            'ry',
            'rz',
            'vx',
            'vy',
            'vz',
            'semi_major_axis',
            'eccentricity',
            'inclination',
            'ascending_node',
            'argument_of_periapsis',
            'true_anomaly',
        ]
        names = kwargs.get('names', default_names)
        self.interpolate = interpolate
        self.s0 = s0
        self._states = np.vstack(states)
        self.spline = interp1d(dt, self._states, kind='cubic')
        if interpolate:
            t = np.linspace(0.0, dt[-1], interpolate)
            epochs = s0.t + TimeDelta(t, format='sec')
            y = self.spline(t)
            rx = y[0,:]
            ry = y[1,:]
            rz = y[2,:]
            vx = y[3,:]
            vy = y[4,:]
            vz = y[5,:]
        else:
            rx, ry, rz, vx, vy, vz = states
            t = dt

        if not elements:
            elements = kepler.elements(
                s0.body.mu,
                np.column_stack((rx, ry, rz))*s0.r.unit,
                np.column_stack((vx, vy, vz))*s0.v.unit,
            )

        sma, ecc, inc, node, peri, ano = elements
        columns = [t, epochs, rx, ry, rz, vx, vy, vz, sma, ecc, inc, node, peri, ano]
        self.table = Table(columns, names=names)

    @property
    def epoch(self):
        return self.table['epoch']

    @property
    def dt(self):
        return self.table['dt']

    @property
    def rx(self):
        return self.table['rx']

    @property
    def ry(self):
        return self.table['ry']

    @property
    def rz(self):
        return self.table['rz']

    @property
    def vx(self):
        return self.table['vx']

    @property
    def vy(self):
        return self.table['vy']

    @property
    def vz(self):
        return self.table['vz']

    @property
    def semi_major_axis(self):
        return self.table['semi_major_axis']

    @property
    def eccentricity(self):
        return self.table['eccentricity']

    @property
    def inclination(self):
        return self.table['inclination']

    @property
    def ascending_node(self):
        return self.table['ascending_node']

    @property
    def argument_of_periapsis(self):
        return self.table['argument_of_periapsis']

    @property
    def true_anomaly(self):
        return self.table['true_anomaly']

    def interpolate(self, dt):
        return self.spline(dt)

    def state(self, t):
        arr = self.interpolate(t)
        if arr.ndim == 1:
            return type(self.s0).from_array(arr, t, self.s0) 
        else:
            return [type(self.s0).from_array(e, t, self.s0) for e in arr.T]

    def plot_plane(self, plane='XY'):
        vis.plot_plane(self, plane=plane)

    def plot(self):
        plots = [vis.plot_plane(self, plane=plane, show_plot=False) for plane in ('XY', 'XZ', 'YZ')]
        show(vplot(*plots))

    def plot3d(self):
        vis.plot3d(self)
