import astropy.units as u
from plyades.config import config


# Values taken from:
# Archinal, et al. "Report of the IAU working group on cartographic
# coordinates and rotational elements: 2009." Celestial Mechanics
# and Dynamical Astronomy 109.2 (2011): 101-135.
#
# Archinal, et al. "Erratum to: Reports of the IAU Working Group on
# Cartographic Coordinates and Rotational Elements: 2006 & 2009."
# Celestial Mechanics and Dynamical Astronomy 110.4 (2011): 401-403.

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
        jpl_id,
        symbol,
        # rotational_elements,
    ):
        self.name = name
        self.mu = mu
        self.mean_radius = mean_radius
        self.equatorial_radius = equatorial_radius
        self.polar_radius = polar_radius
        self.jpl_id = jpl_id
        self.symbol = symbol
        # self._rotational_elements = rotational_elements

    def _repr_html_(self):
        strs = [
            "<h2>{} {}</h2>".format(self.name, self.symbol),
            "Gravitational parameter ($\mu$): {}".format(self.mu._repr_latex_()),
            "Mean radius ($r_m$): {}".format(self.mean_radius),
            "Equatorial radius ($r_e$): {}".format(self.equatorial_radius),
            "Polar radius ($r_p$): {}".format(self.polar_radius),
        ]
        return "<br />".join(strs)

    def rv(self, jd, jd2=0.0):
        return config['ephemeris'].rv(self.jpl_id, jd, jd2)

    def wrt(self, body, jd, jd2=0.0):
        r_target, v_target = self.rv(jd, jd2)
        r_origin, v_origin = body.rv(jd, jd2)
        return r_target-r_origin, v_target-v_origin


class Moon:
    pass


class SmallBody:
    pass

MERCURY = Planet(
    'Mercury',
    0.0*u.km**3/u.s**2,
    2439.7*u.km,
    2439.7*u.km,
    2439.7*u.km,
    199,
    u"\u263F",
)
VENUS = Planet(
    'Venus',
    0.0*u.km**3/u.s**2,
    6051.8*u.km,
    6051.8*u.km,
    6051.8*u.km,
    299,
    u"\u2640",
)
EARTH = Planet(
    'Earth',
    398600.4418*u.km**3/u.s**2,
    6371.0084*u.km,
    6378.1366*u.km,
    6356.7519*u.km,
    399,
    u"\u2641",
)
MARS = Planet(
    'Mars',
    0.0*u.km**3/u.s**2,
    3389.50*u.km,
    3396.19*u.km,
    3376.20*u.km,
    4,
    u"\u2642",
)
JUPITER = Planet(
    'Jupiter',
    0.0*u.km**3/u.s**2,
    69911.0*u.km,
    71492.0*u.km,
    66854.0*u.km,
    5,
    u"\u2643",
)
SATURN = Planet(
    'Saturn',
    0.0*u.km**3/u.s**2,
    58232.0*u.km,
    60268.0*u.km,
    54364.0*u.km,
    6,
    u"\u2644",
)
URANUS = Planet(
    'Uranus',
    0.0*u.km**3/u.s**2,
    25362.0*u.km,
    25559.0*u.km,
    24973.0*u.km,
    7,
    u"\u26E2",
)
NEPTUNE = Planet(
    'Neptune',
    0.0*u.km**3/u.s**2,
    24622.0*u.km,
    24764.0*u.km,
    24341.0*u.km,
    8,
    u"\u2646",
)
