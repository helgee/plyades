from .ephemerides import AnalyticalEphemeris, NumericalEphemeris
import astropy.units as u

config = {'ephemeris': AnalyticalEphemeris()}

def load_kernel(file, units=(u.km, u.km/u.s)):
    config['ephemeris'] = NumericalEphemeris(file, units)

