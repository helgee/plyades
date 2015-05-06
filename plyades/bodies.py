import abc
import astropy.units as u
# import astropy.constants as astconst


symbols = {
    "Sun": u"\u2609", "Mercury": u"\u263F", "Venus": u"\u2640",
    "Earth": u"\u2641", "Mars": u"\u2642", "Jupiter": u"\u2643",
    "Saturn": u"\u2644", "Uranus": u"\u26E2", "Neptune": u"\u2646",
    "Moon": u"\u263E", "Pluto": u"\u2647"}


class Body(abc.ABC):
    @abc.abstractmethod
    def wrt(self, body):
        pass


class Planet(Body):
    def __init__(self, mu):
        self.mu = mu

    def wrt(self, body):
        pass


class LibrationPoint(Body):
    pass


class Moon(Body):
    pass


class SmallBody(Body):
    pass

EARTH = Planet(398600.4418*u.km**3/u.s**2)
