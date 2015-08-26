import numpy as np
from astropy.time import Time
from astropy import units as u
import plyades.orbit as orbit
from plyades.bodies import EARTH


class State:
    def __init__(self, r, v, t, frame="MEE2000", body=EARTH):
        self.r = r
        self.v = v
        self.t = Time(t)
        self.frame = frame
        self.body = body
        self._array = np.vstack((np.array(r), np.array(v)))
        self._units = (r.unit, v.unit)

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
        return self.jd - constants.epoch["jd2000"]

    @property
    def jd1950(self):
        return self.jd - constants.epoch["jd1950"]

    @property
    def mjd(self):
        return self.jd - constants.epoch["mjd"]

    @property
    def elements(self):
        return orbit.elements(self.body.mu, self.r, self.v)

    @property
    def period(self):
        return orbit.period(self.elements[0], self.body.mu)


    def propagate(self, dt=None, revolutions=1, step=1):
        s0 = np.atleast_2d(self.state)[0,:]
        t0 = np.atleast_1d(self.t)[0]
        mu = const.planets[self.body.lower()]["mu"]
        if self.solver == "kepler":
            ele = orbit.elements(s0, mu)
            if dt is None:
                tend = orbit.period(ele[0], mu)
                dt = np.arange(step,tend,step)
            elements = np.vstack((ele, orbit.kepler(ele, dt, mu)))
            self.t = [t0 + datetime.timedelta(seconds=t) for t in dt]
            self.t.insert(0,t0)
            self.state = orbit.vector(elements, mu)

    def plot(self):
        n = 100
        elements = np.zeros((n, 6))
        elements[:,6] = np.linspace(-np.pi, np.pi, 100)
        sma, ecc, inc, node, peri, _ = self.elements

        fig = plt.figure("Plyades Plot")
        ax = fig.add_subplot(111, projection='3d')
        re = self.body.equatorial_radius
        rp = self.body.polar_radius

        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        x = re * np.outer(np.cos(u), np.sin(v))
        y = re * np.outer(np.sin(u), np.sin(v))
        z = rp * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b', alpha=.3, linewidth=1, edgecolor="b")
        ax.plot(self.state[:,0], self.state[:,1], self.state[:,2], color="r")

        plt.show()
