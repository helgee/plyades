from __future__ import division
from scipy import optimize
import numpy as np
import util


def rhs(s, t):
    pass

def elements(vector, mu):
    r = np.atleast_2d(vector)[:, 0:3]
    v = np.atleast_2d(vector)[:, 3:6]
    r_mag = util.mag(r)
    v_mag = util.mag(v)
    h = np.cross(r, v)
    h_mag = util.mag(h)
    k = np.array([[0, 0, 1]]).repeat(r.shape[0], axis=0)
    n = np.cross(k, h)
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
    n_ix = n[:, 1] < 0 
    if n_ix.any():
        node[n_ix] = 2 * np.pi - node[n_ix]
    p_ix = e[:, 2] < 0 
    if p_ix.any():
        peri[p_ix] = 2 * np.pi - peri[p_ix]
    a_ix = util.dot(r, v) < 0
    if a_ix.any():
        ano[a_ix] = 2 * np.pi - ano[a_ix]
    # Return a 1D vector if the input was 1-dimensional.
    if vector.shape == (6, ):
        return np.hstack((sma, ecc, inc, node, peri, ano)).flatten()
    else:
        return np.hstack((sma, ecc, inc, node, peri, ano))


def vector(elements, mu):
    ele = np.atleast_2d(elements)
    sma = ele[:, 0, np.newaxis]
    ecc = ele[:, 1, np.newaxis]
    inc = ele[:, 2, np.newaxis]
    node = ele[:, 3, np.newaxis]
    peri = ele[:, 4, np.newaxis]
    ano = ele[:, 5, np.newaxis]
    u = peri + ano

    p = sma * (1 - np.square(ecc))
    e_ix = ecc == 1
    if e_ix.any():
        p[e_ix] = sma[e_ix]

    r = p / (1 + ecc * np.cos(ano))
    x = r * (np.cos(node) * np.cos(u) - np.sin(node) * np.cos(inc) * np.sin(u))
    y = r * (np.sin(node) * np.cos(u) + np.cos(node) * np.cos(inc) * np.sin(u))
    z = r * np.sin(inc) * np.sin(u)
    vr = np.sqrt(mu / p) * ecc * np.sin(ano)
    vf = np.sqrt(mu * p) / r
    vx = (vr * (np.cos(node) * np.cos(u) - np.sin(node) * np.cos(inc) * np.sin(u))
         - vf * (np.cos(node) * np.sin(u) + np.sin(node) * np.cos(u) * np.cos(inc)))
    vy = (vr * (np.sin(node) * np.cos(u) + np.cos(node) * np.cos(inc) * np.sin(u))
         - vf * (np.sin(node) * np.sin(u) - np.cos(node) * np.cos(u) * np.cos(inc)))
    vz = vr * np.sin(inc) * np.sin(u) + vf * np.cos(u) * np.sin(inc)
    if elements.shape == (6, ):
        return np.hstack((x, y, z, vx, vy, vz)).flatten()
    else:
        return np.hstack((x, y, z, vx, vy, vz))

def solve_kepler(mean, ecc):
    def kepler_eq(ecc_ano):
        return ecc_ano - ecc * np.sin(ecc_ano) - mean
    def kepler_eq_der(ecc_ano):
        return 1 - ecc * math.cos(ecc_ano)
    return optimize.newton(kepler_eq,mean, kepler_eq_der, args=(), tol=1e-10, maxiter=50)

def kepler():
    pass

