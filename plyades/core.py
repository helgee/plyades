from bokeh.io import vplot
from bokeh.plotting import show
from copy import deepcopy
import numpy as np
from astropy import units as units
from astropy.time import Time, TimeDelta

from plyades.bodies import EARTH
from plyades.propagator import Propagator
from plyades.orbit import Orbit
import plyades.kepler as kepler
import plyades.forces as forces
import plyades.util as util
import plyades.visualization as vis


class State:
    def __init__(self, r, v, t, frame="MEE2000", body=EARTH, vars=None):
        r_unit = util.getunit(r)
        v_unit = util.getunit(v)
        if not r_unit:
            self.r = r*units.km
        else:
            self.r = r
        if not v_unit:
            self.v = v*units.km/units.s
        else:
            self.v = v
        self.t = Time(t)
        self.frame = frame
        self.body = body
        self._array = np.hstack((np.copy(r), np.copy(v)))
        self._gravity = forces.newton
        self._forces = []
        if vars:
            self.vars = vars

    def force(self, func):
        self._forces.append(func)

    def gravity(self, func):
        self._gravity = func

    @classmethod
    def from_array(cls, arr, t, s0=None):
        if s0:
            frame = s0.frame
            body = s0.body
            t = s0.t + TimeDelta(t, format='sec')
        if len(arr) > 6:
            vars = arr[6:]
        else:
            vars = None
        return cls(
            arr[:3], arr[3:], t,
            frame, body, vars)

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
        self.r = self._array[:3]*self.r.unit
        self.v = self._array[3:]*self.v.unit

    def print_elements(self):
        kepler.print_elements(self.elements)

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
        return kepler.elements(self.body.mu, self.r, self.v)

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
        return kepler.period(self.semi_major_axis, self.body.mu)

    @property
    def orbital_energy(self):
        return kepler.orbital_energy(self.semi_major_axis, self.body.mu)

    @property
    def mean_motion(self):
        return 2*np.pi*units.rad/self.period

    def kepler_orbit(self, n=100):
        dt = np.linspace(0, self.period, n)
        sma, ecc, inc, node, peri, ano1 = self.elements
        mean_ano = kepler.true_to_mean(ano1, ecc)
        mean_ano1 = dt*self.mean_motion + mean_ano
        ano = units.Quantity([kepler.mean_to_true(m, ecc) for m in mean_ano1])
        sma = np.repeat(sma, n)
        ecc = np.repeat(ecc, n)
        inc = np.repeat(inc, n)
        node = np.repeat(node, n)
        peri = np.repeat(peri, n)
        epochs = self.t + TimeDelta(dt, format='sec')
        states = kepler.cartesian(self.body.mu, sma, ecc, inc, node, peri, ano)
        return Orbit(
            deepcopy(self), dt, epochs, states,
            elements=[sma, ecc, inc, node, peri, ano]
        )

    def kepler_state(self, dt):
        sma, ecc, inc, node, peri, true_ano = self.elements
        mean_ano = kepler.true_to_mean(true_ano, ecc)
        mean_ano1 = dt*self.mean_motion + mean_ano
        true_ano1 = kepler.mean_to_true(mean_ano1, ecc) 
        rv = kepler.cartesian(self.body.mu, sma, ecc, inc, node, peri, true_ano1)
        return State(rv[:3]*self.r.unit, rv[3:]*self.v.unit,
            self.t+TimeDelta(dt, format='sec'),
            self.frame, self.body)

    def propagate(self, dt=1*units.year, time_unit=units.s, interpolate=100, **kwargs):
        tout = [0.0]
        yout = [np.copy(self)]
        p = Propagator(self, dt.to(time_unit).value, **kwargs)
        p.forces = list(self._forces)
        p.forces.append(self._gravity)
        for t, y in p:
            tout.append(t)
            yout.append(y)
        tout = np.array(tout)*time_unit
        yout = np.vstack(yout)
        epochs = self.t + TimeDelta(tout.to(units.s), format='sec')
        return Orbit(deepcopy(self), tout, epochs, yout.T, interpolate=interpolate, **kwargs)
