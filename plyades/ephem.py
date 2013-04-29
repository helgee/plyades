from __future__ import division, print_function
import numpy as np
import jplephem
import de421

Ephemeris = jplephem.Ephemeris(de421)

def select(ephemeris_name):
    valid_names = ("de405", "de406", "de421", "de421", "de423")
    if ephemeris_name not in valid_names:
        raise ValueError(ephemeris_name + " is not a valid ephemeris name.")
    
    try:
        if ephemeris_name == "de421":
            import de421
            Ephemeris = jplephem.Ephemeris(de421)
        elif ephemeris_name == "de422":
            import de422
            Ephemeris = jplephem.Ephemeris(de422)
        elif ephemeris_name == "de423":
            import de423
            Ephemeris = jplephem.Ephemeris(de423)
        elif ephemeris_name == "de405":
            import de405
            Ephemeris = jplephem.Ephemeris(de405)
        elif ephemeris_name == "de406":
            import de406
            Ephemeris = jplephem.Ephemeris(de406)
    except ImportError:
        print("The selected ephemeris was not found on this system.")
        pass

def compute(date, body, origin="sun", velocity=True):
    date = np.asarray(date)
    if body == "earth":
        body = "earthmoon"

    if origin == "earth":
        origin = "earthmoon"

    if velocity:
        body_ephem = np.vstack(Ephemeris.compute(body, date)).T
        body_ephem[:,3:6] = body_ephem[:,3:6] / 86400
    else:
        body_ephem = np.vstack(Ephemeris.position(body, date)).T

    if not origin == "sun" and velocity:
        origin_ephem = np.vstack(Ephemeris.compute(origin, date)).T
        origin_ephem[:,3:6] = origin_ephem[:,3:6] / 86400
    elif not origin == "sun":
        origin_ephem = np.vstack(Ephemeris.position(origin, date)).T

    if not origin == "sun":
        ephem = body_ephem - origin_ephem
    else:
        ephem = body_ephem

    if len(ephem) == 1:
        return ephem.flatten()
    else:
        return ephem
