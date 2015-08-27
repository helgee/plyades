import numpy as np
from astropy.time import Time, TimeDelta
from astropy import units as units
import plyades.orbit as orbit
import plyades.util as util
from plyades.bodies import EARTH
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from bokeh.io import vplot
from bokeh.plotting import figure, show

class State:
    def __init__(self, r, v, t, frame="MEE2000", body=EARTH):
        self.r = r
        self.v = v
        self.t = Time(t)
        self.frame = frame
        self.body = body
        self._array = np.vstack((np.array(r), np.array(v)))
        self._units = (r.unit, v.unit)
        self.plot_height = 500
        self.plot_width = 500

    def __array__(self):
        return self._array

    def __iter__(self):
        yield from self._array

    def __len__(self):
        return len(self._array)

    def __getitem__(self, position):
        return self._array[position]

    def __setitem__(self, position, value):
        self._array[position] = value
        self.r = self._array[:3]*self._units[0]
        self.v = self._array[3:]*self._units[1]

    def print_elements(self):
        orbit.print_elements(self.elements)

    def wrt(self, body):
        r_origin, v_origin = body.rv(self.t.jd, self.t.jd2)
        return self.r-r_origin, self.v-v_origin

    @property
    def jd(self):
        return self.t.jd

    @property
    def jd2000(self):
        return self.jd - constants.DELTA_JD2000

    @property
    def jd1950(self):
        return self.jd - constants.DELTA_JD1950

    @property
    def mjd(self):
        return self.jd - constants.DELTA_MJD

    @property
    def elements(self):
        return orbit.elements(self.body.mu, self.r, self.v)

    @property
    def semi_major_axis(self):
        return self.elements[0]

    @property
    def eccentricity(self):
        return self.elements[1]

    @property
    def inclination(self):
        return self.elements[2]

    @property
    def ascending_node(self):
        return self.elements[3]

    @property
    def argument_of_periapsis(self):
        return self.elements[4]

    @property
    def true_anomaly(self):
        return self.elements[5]

    @property
    def period(self):
        return orbit.period(self.semi_major_axis, self.body.mu)

    @property
    def orbital_energy(self):
        return orbit.orbital_energy(self.semi_major_axis, self.body.mu)

    @property
    def mean_motion(self):
        return 2*np.pi*units.rad/self.period

    def solve_kepler(self, dt):
        sma, ecc, inc, node, peri, true_ano = self.elements
        mean_ano = orbit.true_to_mean(true_ano, ecc)
        mean_ano1 = dt*self.mean_motion + mean_ano
        true_ano1 = orbit.mean_to_true(mean_ano1, ecc) 
        rv = orbit.cartesian(self.body.mu, sma, ecc, inc, node, peri, true_ano1)
        return State(rv[:3]*self.r.unit, rv[3:]*self.v.unit,
            self.t+TimeDelta(dt, format='sec'),
            self.frame, self.body)

    def kepler(self, n=100):
        sma, ecc, inc, node, peri, ano1 = self.elements
        ano = np.linspace(0,  2*np.pi, n)*units.rad
        sma = np.repeat(sma, n)
        ecc = np.repeat(ecc, n)
        inc = np.repeat(inc, n)
        node = np.repeat(node, n)
        peri = np.repeat(peri, n)
        return orbit.cartesian(self.body.mu, sma, ecc, inc, node, peri, ano)

    def plot_plane(self, plane='XY', show_plot=True):
        x, y, z, *_ = self.kepler()
        r = self.body.mean_radius.value
        if plane == 'XY':
            x, y, z = x.value, y.value, z.value
            xs = self.r[0].value
            ys = self.r[1].value
        elif plane == 'XZ':
            x, y, z = x.value, z.value, y.value
            xs = self.r[0].value
            ys = self.r[2].value
        elif plane == 'YZ':
            x, y, z = y.value, z.value, x.value
            xs = self.r[1].value
            ys = self.r[2].value

        magnitudes = np.sqrt(np.square(x)+np.square(y))
        limit = np.maximum(r, magnitudes.max()) * 1.2
        f = figure(
            height = self.plot_height,
            width = self.plot_width,
            title = plane,
            x_range = (-limit, limit),
            y_range = (-limit, limit),
        )
        ind = (magnitudes < r) & (z < 0)
        start = -np.flatnonzero(ind)[0]
        x_bg = x[ind]
        y_bg = y[ind]
        x_fg = x[~ind]
        y_fg = y[~ind]
        x_bg = np.roll(x_bg, start)
        y_bg = np.roll(y_bg, start)
        x_fg = np.roll(x_fg, start)
        y_fg = np.roll(y_fg, start)
        f.circle(x=0, y=0, radius=r, alpha=0.5)
        f.line(x_fg, y_fg, line_width=2, color='darkblue')
        f.circle(x_bg, y_bg, size=2, color='darkblue')
        f.circle(x=xs, y=ys, size=10, color='purple')
        if show_plot:
            show(f)
        else:
            return f

    def plot(self):
        plots = (self.plot_plane(plane, show_plot=False) for plane in ('XY', 'XZ', 'YZ'))
        show(vplot(*plots))

    def plot3d(self):
        x, y, z, *_ = self.kepler()

        fig = plt.figure("Plyades Plot", figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        self.body.plot3d(ax)
        ax.plot(x, y, zs=z, color="r")

        plt.show()
