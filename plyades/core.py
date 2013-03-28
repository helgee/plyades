from __future__ import division, print_function
import datetime
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import const
import time
import orbit


# Too much problems with Python 2.X
# symbols = {"Sun": u"\u2609", "Mercury": u"\u263F", "Venus": u"\u2640", "Earth": u"\u2641",
#            "Mars": u"\u2642", "Jupiter": u"\u2643", "Saturn": u"\u2644", "Uranus": u"\u26E2",
#            "Neptune": u"\u2646", "Moon": u"\u263E"}

class State(object):
    def __init__(self, rv, t=datetime.datetime(2000,1,1), body="Earth", frame="MEE2000"):
        self.rv = rv
        self._rv = rv
        self.t = t
        self.body = body
        self._body = body
        self._frame = frame
        self.frame = frame

    def __repr__(self):
        rv = self.rv.__repr__()
        t = self.t.__repr__()
        body = self.body.__repr__()
        frame = self.frame.__repr__()
        return "State({}, t={}, body={}, frame={})".format(rv, t, body, frame)

    def __str__(self):
        strings = ["{:<17}{}".format("Epoch:", self.t), "{:<17}{}".format("Reference frame:", self.frame),
                   "{:<17}{}".format("Central body:", self.body), ""]
        names = ["x [km]:", "y [km]:", "z [km]:", "vx [km/s]:", "vy [km/s]:", "vz [km/s]:"]
        values = self.rv
        strings.extend(["{:<11}{:>20,.5f}".format(name, value) for name, value in zip(names, values)])
        return "\n".join(strings)

    def print_elements(self):
        orbit.print_elements(self.elements)

    @property
    def jd(self):
        return time.datetime2jd(self.t)

    @property
    def jd2000(self):
        return self.jd - const.epoch["jd2000"]

    @property
    def jd1950(self):
        return self.jd - const.epoch["jd1950"]

    @property
    def mjd(self):
        return self.jd - const.epoch["mjd"]

    @property
    def r(self):
        return self.rv[0:3]

    @property
    def v(self):
        return self.rv[3:6]

    @property
    def elements(self):
        mu = const.planets[self.body.lower()]["mu"]
        return orbit.elements(self.rv, mu)

    @property
    def period(self):
        mu = const.planets[self.body.lower()]["mu"]
        return orbit.period(self.elements[0], mu)

class Orbit:
    def __init__(self, state, options=None, t=None):
        if options is None:
            options = {}
        self.body = options.get("body", "Earth")
        self.frame = options.get("frame", "MEE2000")
        self.solver = options.get("solver", "kepler")
        self.t = getattr(state, "t", t)
        if self.t is None:
            raise ValueError("Initial epoch has not been set.")
        self.state = getattr(state, "rv", state)

    def __str__(self):
        string = ["Orbit at initial epoch:"]
        return "\n".join(string)

    @property
    def elements(self):
        mu = const.planets[self.body.lower()]["mu"]
        return orbit.elements(self.state, mu)

    def propagate(self, dt=None, revolutions=1, step=1):
        s0 = np.atleast_2d(self.state)[0,:]
        t0 = np.atleast_1d(self.t)[0]
        mu = const.planets[self.body.lower()]["mu"]
        if self.solver == "kepler":
            ele = orbit.elements(s0, mu)
            if dt is None:
                tend = orbit.period(ele[0], mu)
                dt = np.arange(step,tend,step)
            self.elements = np.vstack((ele, orbit.kepler(ele, dt, mu)))
            self.t = [t0 + datetime.timedelta(seconds=t) for t in dt]
            self.t.insert(0,t0)
            self.state = orbit.vector(self.elements, mu)

    def plot(self):
        fig = plt.figure("Plyades Plot")
        ax = fig.add_subplot(111, projection='3d')
        re = const.planets[self.body.lower()]["re"]
        rp = const.planets[self.body.lower()]["rp"]

        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        x = re * np.outer(np.cos(u), np.sin(v))
        y = re * np.outer(np.sin(u), np.sin(v))
        z = rp * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b', alpha=.3, linewidth=1, edgecolor="b")
        ax.plot(self.state[:,0], self.state[:,1], self.state[:,2], color="r")

        plt.show()
