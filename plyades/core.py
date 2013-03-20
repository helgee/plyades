from __future__ import division, print_function
import collections
import datetime
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import constants
import const
import time
import orbit


# Too much problems with Python 2.X
# symbols = {"Sun": u"\u2609", "Mercury": u"\u263F", "Venus": u"\u2640", "Earth": u"\u2641",
#            "Mars": u"\u2642", "Jupiter": u"\u2643", "Saturn": u"\u2644", "Uranus": u"\u26E2",
#            "Neptune": u"\u2646", "Moon": u"\u263E"}

class Epoch(datetime.datetime):
    @property
    def jd(self):
        return time.datetime2jd(self)

    @property
    def jd2000(self):
        return self.jd - constants.epoch.jd2000

    @property
    def jd1950(self):
        return self.jd - constants.epoch.jd1950

    @property
    def mjd(self):
        return self.jd - constants.epoch.mjd

    @classmethod
    def fromdatetime(cls, dt):
        if dt.tzinfo is not None:
            raise ValueError("Datetime is expected to be in UTC and timezone unaware.")
        else:
            return cls(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)
        


class State(np.ndarray):
    def __new__(cls, rv, t=Epoch(2000,1,1), body="Earth", frame="MEE2000"):
        obj = np.asarray(rv).view(cls)
        obj.t = t
        obj.body = body
        obj.frame = frame
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.t = getattr(obj, "t", Epoch(2000,1,1))
        self.body = getattr(obj, "body", "Earth")
        self.frame = getattr(obj, "frame", "MEE2000")

    def __repr__(self):
        rv = self.rv.__repr__()
        t = self.t.__repr__()
        body = self.body.__repr__()
        frame = self.frame.__repr__()
        return "State({}, t={}, body={}, frame={})".format(rv, t, body, frame)

    def __str__(self):
        string = []
        string.append("Epoch: {}")
        string.append("Reference frame: {}")
        string.append("Central body: {}")
        string.append("x [km]: {}")
        string.append("y [km]: {}")
        string.append("z [km]: {}")
        string.append("vx [km/s]: {}")
        string.append("vy [km/s]: {}")
        string.append("vz [km/s]: {}")
        return "\n".join(string).format(self.t, self.frame, self.body, *self)

    @property
    def r(self):
        return np.asarray(self)[0:3]

    @property
    def v(self):
        return np.asarray(self)[3:6]

    @property
    def rv(self):
        return np.asarray(self)

class Orbit:
    def __init__(self, state, options=None, t=None):
        if options is None:
            options = {}
        self.body = options.get("body", "Earth")
        self.frame = options.get("frame", "MEE2000")
        self.solver = options.get("solver", "kepler")
        self.t = [getattr(state, 't', t)]
        if self.t is None:
            raise ValueError("Initial epoch has not been set!")
        self.state = state.rv

    def propagate(self, dt=None, revolutions=1, step=1):
        s0 = np.atleast_2d(self.state)[0,:]
        t0 = self.t[0]
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
        r = const.planets[self.body.lower()]["req"]

        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        x = r * np.outer(np.cos(u), np.sin(v))
        y = r * np.outer(np.sin(u), np.sin(v))
        z = r * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b', alpha=.3, linewidth=1, edgecolor="b")
        ax.plot(self.state[:,0], self.state[:,1], self.state[:,2], color="r")

        plt.show()
