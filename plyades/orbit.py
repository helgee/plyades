from astropy.table import Table
from astropy.time import TimeDelta
import astropy.units as units
from bokeh.plotting import show, figure
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
        self._states = np.array(states)
        self.spline = interp1d(dt, self._states, kind='cubic')
        if interpolate:
            t = np.linspace(0.0, dt[-1], interpolate)
            epochs = s0.t + TimeDelta(t, format='sec')
            y = self.spline(t)
            rx = y[0,:]*s0.r.unit
            ry = y[1,:]*s0.r.unit
            rz = y[2,:]*s0.r.unit
            vx = y[3,:]*s0.v.unit
            vy = y[4,:]*s0.v.unit
            vz = y[5,:]*s0.v.unit
        else:
            rx, ry, rz, vx, vy, vz = self._states
            t = dt

        if not elements:
            elements = kepler.elements(
                s0.body.mu,
                np.array((rx, ry, rz)).T*s0.r.unit,
                np.array((vx, vy, vz)).T*s0.v.unit,
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

    def plot_plane(self, plane='XY', show_steps=True):
        vis.plot_plane(self, plane=plane, show_steps=show_steps)

    def plot(self):
        plots = [vis.plot_plane(self, plane=plane, show_plot=False) for plane in ('XY', 'XZ', 'YZ')]
        show(vplot(*plots))

    def plot3d(self):
        vis.plot3d(self)

    def plot_element(self, element, show_plot=True):
        if element == 'semi_major_axis':
            y = self.table[element].quantity
            f = figure(
                x_axis_type='datetime',
                width=500,
                height=500,
                title = 'Semi-major axis',
            )
        elif element == 'eccentricity':
            y = self.table[element].quantity
            f = figure(
                x_axis_type='datetime',
                width=500,
                height=500,
                title = 'Eccentricity',
            )
        elif element == 'inclination':
            y = self.table[element].to(units.deg)
            f = figure(
                x_axis_type='datetime',
                y_range=(0, 180),
                width=500,
                height=500,
                title = 'Inclination',
            )
        elif element == 'ascending_node':
            y = self.table[element].to(units.deg)
            f = figure(
                y_range=(0, 360),
                x_axis_type='datetime',
                width=500,
                height=500,
                title = 'Longitude of ascending node',
            )
        elif element == 'argument_of_periapsis':
            y = self.table[element].to(units.deg)
            f = figure(
                y_range=(0, 360),
                x_axis_type='datetime',
                width=500,
                height=500,
                title = 'Argument of periapsis',
            )
        elif element == 'true_anomaly':
            y = self.table[element].to(units.deg)
            f = figure(
                x_axis_type='datetime',
                y_range=(0, 180),
                width=500,
                height=500,
                title = 'True anomaly',
            )

        f.line(x=self.epoch.datetime, y=y.value, line_width=2)
        if show_plot:
            show(f)
        else:
            return f


    def plot_elements(self):
        elements = (
            'semi_major_axis',
            'eccentricity',
            'inclination',
            'ascending_node',
            'argument_of_periapsis',
            'true_anomaly',
        )
        plots = [self.plot_element(element, show_plot=False) for element in elements]
        show(vplot(*plots))
