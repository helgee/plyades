from __future__ import division
import numpy as np
import util


def rhs(s, t):
    pass


class Propagator:
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
    if vector.shape == (1, 1):
        return np.hstack([sma, ecc, inc, node, peri, ano]).flatten()
    else:
        return np.hstack([sma, ecc, inc, node, peri, ano])


def vector(elements, mu):
    pass
