from __future__ import division, print_function
from scipy import optimize
import numpy as np
import plyades.util as util

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

def elements(mu, r, v):
    r = np.atleast_2d(r)
    v = np.atleast_2d(v)
    r_mag = util.mag(r)
    v_mag = util.mag(v)
    h = util.cross(r, v)
    h_mag = util.mag(h)
    k = np.array([[0, 0, 1]]).repeat(r.shape[0], axis=0)
    n = util.cross(k, h)
    n_mag = util.mag(n)
    xi = v_mag ** 2 / 2 - mu / r_mag
    e = ((v_mag ** 2 - mu / r_mag) * r - v * util.dot(r, v)) / mu
    ecc = util.mag(e)
    if not (ecc == 1).any():
        sma = - mu / (2 * xi)
        p = sma * (1 - ecc ** 2)
    else:
        p = h_mag ** 2 / mu
        sma = p
    inc = np.arccos(h[:, 2, np.newaxis] / h_mag)
    node = np.arccos(n[:, 0, np.newaxis] / n_mag)
    peri = np.arccos(util.dot(n, e) / (ecc * n_mag))
    ano = np.arccos(util.dot(e, r) / (ecc * r_mag))
    # Quadrant checks
    node = util.mod2pi(node)
    peri = util.mod2pi(peri)
    ano = util.mod2pi(ano)
    return (
        sma.squeeze(), ecc.squeeze(), inc.squeeze(),
        node.squeeze(), peri.squeeze(), ano.squeeze())


def print_elements(ele):
    names = ["Semi-major axis:", "Eccentricity:", "Inclination:",
             "Ascending node:", "Argument of perigee:",
             "True anomaly:"]
    for name, element in zip(names[:2], ele[:2]):
        print("{:<26}{:>16.5f}".format(name, element))
    for name, element in zip(names[2:], ele[2:]):
        print("{:<26}{:>16.5f}".format(name, np.degrees(element)))


def vector(mu, sma, ecc, inc, node, peri, ano):
    u = peri + ano

    p = sma * (1 - np.square(ecc))
    e_ix = ecc == 1
    if e_ix.any():
        p[e_ix] = sma[e_ix]

    r = p / (1 + ecc * np.cos(ano))
    x = r*(np.cos(node)*np.cos(u) - np.sin(node)*np.cos(inc)*np.sin(u))
    y = r*(np.sin(node)*np.cos(u) + np.cos(node)*np.cos(inc)*np.sin(u))
    z = r*np.sin(inc)*np.sin(u)
    vr = np.sqrt(mu/p)*ecc*np.sin(ano)
    vf = np.sqrt(mu*p)/r
    vx = (
        vr*(np.cos(node)*np.cos(u) - np.sin(node)*np.cos(inc)*np.sin(u)) -
        vf*(np.cos(node)*np.sin(u) + np.sin(node)*np.cos(u)*np.cos(inc)))
    vy = (
        vr*(np.sin(node)*np.cos(u) + np.cos(node)*np.cos(inc)*np.sin(u)) -
        vf*(np.sin(node)*np.sin(u) - np.cos(node)*np.cos(u)*np.cos(inc)))
    vz = vr*np.sin(inc)*np.sin(u) + vf*np.cos(u)*np.sin(inc)
    return (
        x.squeeze(), y.squeeze(), z.squeeze(),
        vx.squeeze(), vy.squeeze(), vz.squeeze())


def period(a, mu):
    return np.sqrt(4 * a**3 * np.pi**2 / mu)


def ecc2true(E, e):
    return 2*np.arctan2(np.sqrt(1 + e)*np.sin(E/2), np.sqrt(1 - e)*np.cos(E/2))


def true2ecc(T, e):
    return 2*np.arctan2(np.sqrt(1 - e)*np.sin(T/2), np.sqrt(1 + e)*np.cos(T/2))


def ecc2mean(E, e):
    return E - e*np.sin(E)


def mean2ecc(M, e):
    def kepler_eq(E):
        return E - e*np.sin(E) - M

    def kepler_eq_der(E):
        return 1 - e*np.cos(E)

    return optimize.newton(
        kepler_eq, M, kepler_eq_der, args=(), tol=1e-10, maxiter=50)


def kepler(ele, dt, mu):
    E0 = true2ecc(ele[5], ele[1])
    M0 = ecc2mean(E0, ele[1])
    n = 2*np.pi/period(ele[0], mu)
    M = M0 + n*dt
    if not np.isscalar(M):
        E = np.zeros(np.shape(M))
        out = np.zeros((len(M), 6))
        for i, m in enumerate(M):
            E[i] = mean2ecc(m, ele[1])
    else:
        out = np.zeros((1, 6))
        E = mean2ecc(M, ele[1])
    T = ecc2true(E, ele[1])
    out[:, 0:5] = ele[0:5]
    out[:, 5] = T
    if out.shape == (6, ):
        return out.flatten()
    else:
        return out
