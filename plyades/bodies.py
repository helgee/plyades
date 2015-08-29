import astropy.units as u
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from plyades.config import config


# Values taken from:
# Archinal, et al. "Report of the IAU working group on cartographic
# coordinates and rotational elements: 2009." Celestial Mechanics
# and Dynamical Astronomy 109.2 (2011): 101-135.
#
# Archinal, et al. "Erratum to: Reports of the IAU Working Group on
# Cartographic Coordinates and Rotational Elements: 2006 & 2009."
# Celestial Mechanics and Dynamical Astronomy 110.4 (2011): 401-403.
#
# Vallado, David A., and Wayne D. McClain.
# Fundamentals of astrodynamics and applications.
# Fourth Edition. Springer Science & Business Media, 2013.

# symbols = {
#     "Sun": u"\u2609", "Mercury": u"\u263F", "Venus": u"\u2640",
#     "Earth": u"\u2641", "Mars": u"\u2642", "Jupiter": u"\u2643",
#     "Saturn": u"\u2644", "Uranus": u"\u26E2", "Neptune": u"\u2646",
#     "Moon": u"\u263E", "Pluto": u"\u2647"}


class Planet:
    def __init__(
        self,
        name,
        mu,
        mean_radius,
        equatorial_radius,
        polar_radius,
        j2,
        jpl_id,
        symbol,
        # rotational_elements,
    ):
        self.name = name
        self.mu = mu
        self.mean_radius = mean_radius
        self.equatorial_radius = equatorial_radius
        self.polar_radius = polar_radius
        self.j2 = j2
        self.jpl_id = jpl_id
        self.symbol = symbol
        # self._rotational_elements = rotational_elements

    def _repr_latex_(self):
        strs = [
            "{} {}".format(self.name, self.symbol),
            "Gravitational parameter:",
            "$\mu={}$ {}".format(self.mu.value, self.mu.unit),
            "Mean radius:",
            "$r_m={}$: {}".format(self.mean_radius.value, self.mean_radius.unit),
            "Equatorial radius:",
            "$r_e={}$ {}".format(self.equatorial_radius.value, self.equatorial_radius.unit),
            "Polar radius:",
            "$r_p={}$ {}".format(self.polar_radius.value, self.polar_radius.unit),
            "J2:",
            "$J_2={}$".format(self.j2),
        ]
        return "<br />".join(strs)

    def rv(self, jd, jd2=0.0):
        return config['ephemeris'].rv(self.jpl_id, jd, jd2)

    def wrt(self, body, jd, jd2=0.0):
        r_target, v_target = self.rv(jd, jd2)
        r_origin, v_origin = body.rv(jd, jd2)
        return r_target-r_origin, v_target-v_origin

    def plot3d(self, ax=None):
        if not ax:
            fig = plt.figure("Plyades Plot")
            ax = fig.add_subplot(111, projection='3d')
        re = self.equatorial_radius
        rp = self.polar_radius

        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        x = re * np.outer(np.cos(u), np.sin(v))
        y = re * np.outer(np.sin(u), np.sin(v))
        z = rp * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x, y, z,
            rstride=4,
            cstride=4,
            color='b',
            alpha=.3,
            linewidth=1,
            edgecolor="b"
        )


class Moon:
    pass


class SmallBody:
    pass

MERCURY = Planet(
    'Mercury',
    2.2032e4*u.km**3/u.s**2,
    2439.7*u.km,
    2439.7*u.km,
    2439.7*u.km,
    0.00006,
    199,
    u"\u263F",
)
VENUS = Planet(
    'Venus',
    3.257e5*u.km**3/u.s**2,
    6051.8*u.km,
    6051.8*u.km,
    6051.8*u.km,
    0.000027,
    299,
    u"\u2640",
)
EARTH = Planet(
    'Earth',
    398600.4418*u.km**3/u.s**2,
    6371.0084*u.km,
    6378.1366*u.km,
    6356.7519*u.km,
    0.0010826269,
    399,
    u"\u2641",
)
MARS = Planet(
    'Mars',
    4.305e4*u.km**3/u.s**2,
    3389.50*u.km,
    3396.19*u.km,
    3376.20*u.km,
    0.001964,
    4,
    u"\u2642",
)
JUPITER = Planet(
    'Jupiter',
    1.268e8*u.km**3/u.s**2,
    69911.0*u.km,
    71492.0*u.km,
    66854.0*u.km,
    0.01475,
    5,
    u"\u2643",
)
SATURN = Planet(
    'Saturn',
    3.794e7*u.km**3/u.s**2,
    58232.0*u.km,
    60268.0*u.km,
    54364.0*u.km,
    0.01645,
    6,
    u"\u2644",
)
URANUS = Planet(
    'Uranus',
    5.794e6*u.km**3/u.s**2,
    25362.0*u.km,
    25559.0*u.km,
    24973.0*u.km,
    0.012,
    7,
    u"\u26E2",
)
NEPTUNE = Planet(
    'Neptune',
    6.809e6*u.km**3/u.s**2,
    24622.0*u.km,
    24764.0*u.km,
    24341.0*u.km,
    0.004,
    8,
    u"\u2646",
)
