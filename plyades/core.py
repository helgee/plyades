import numpy as np
import plyades.const as const
from astropy.time import Time
from astropy import units as u
import plyades.orbit as orbit
from plyades.bodies import EARTH


class State:
    def __init__(self, array, t, body=EARTH, frame="MEE2000", units=None):
        # if not units:
        #     self.units = [u.km]*3
        #     self.units.extend([u.km/u.s]*3)
        self._array = np.array(array)
        self.t = Time(t)
        self.body = body
        self.frame = frame

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

    def print_elements(self):
        orbit.print_elements(self.elements)

    @property
    def jd(self):
        return self.t.jd

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
        return self[:3]

    @property
    def v(self):
        return self[3:6]

    @property
    def elements(self):
        return orbit.elements(self.body.mu, self[:3]*u.km, self[3:]*u.km/u.s)

    @property
    def period(self):
        return orbit.period(self.elements[0], self.body.mu)


class Orbit:
    pass
#     def __init__(self, state, options=None, t=None):
#         if options is None:
#             options = {}
#         self.body = options.get("body", "Earth")
#         self.frame = options.get("frame", "MEE2000")
#         self.solver = options.get("solver", "kepler")
#         self.t = getattr(state, "t", t)
#         if self.t is None:
#             raise ValueError("Initial epoch has not been set.")
#         self.state = getattr(state, "rv", state)
#
#     def __str__(self):
#         string = ["Orbit at initial epoch:"]
#         return "\n".join(string)
#
#     @property
#     def elements(self):
#         mu = const.planets[self.body.lower()]["mu"]
#         return orbit.elements(self.state, mu)
#
#     def propagate(self, dt=None, revolutions=1, step=1):
#         s0 = np.atleast_2d(self.state)[0,:]
#         t0 = np.atleast_1d(self.t)[0]
#         mu = const.planets[self.body.lower()]["mu"]
#         if self.solver == "kepler":
#             ele = orbit.elements(s0, mu)
#             if dt is None:
#                 tend = orbit.period(ele[0], mu)
#                 dt = np.arange(step,tend,step)
#             elements = np.vstack((ele, orbit.kepler(ele, dt, mu)))
#             self.t = [t0 + datetime.timedelta(seconds=t) for t in dt]
#             self.t.insert(0,t0)
#             self.state = orbit.vector(elements, mu)
#
    # def plot(self):
    #     fig = plt.figure("Plyades Plot")
    #     ax = fig.add_subplot(111, projection='3d')
    #     re = const.planets[self.body.lower()]["re"]
    #     rp = const.planets[self.body.lower()]["rp"]
    #
    #     u = np.linspace(0, 2 * np.pi, 100)
    #     v = np.linspace(0, np.pi, 100)
    #
    #     x = re * np.outer(np.cos(u), np.sin(v))
    #     y = re * np.outer(np.sin(u), np.sin(v))
    #     z = rp * np.outer(np.ones(np.size(u)), np.cos(v))
    #     ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b', alpha=.3, linewidth=1, edgecolor="b")
    #     ax.plot(self.state[:,0], self.state[:,1], self.state[:,2], color="r")
    #
    #     plt.show()
