from __future__ import division
import numpy as np


def rhs(s, t):
    pass


class Propagator:
    pass


def elements(vector, mu):
    r = np.atleast_2d(vector)[:, 0:3]
    v = np.atleast_2d(vector)[:, 3:6]
    r_mag = np.sqrt((r ** 2).sum(axis=1, keepdims=True))
    v_mag = np.sqrt((v ** 2).sum(axis=1, keepdims=True))
    h = np.cross(r, v)
    h_mag = np.sqrt((h ** 2).sum(axis=1, keepdims=True))
    k = np.array([[0, 0, 1]]).repeat(r.shape[0], axis=0)
    n = np.cross(k, h)
    n_mag = np.sqrt((n ** 2).sum(axis=1, keepdims=True))
    xi = v_mag ** 2 / 2 - mu / r_mag
    e = ((v_mag ** 2 - mu / r_mag) * r - v * np.sum(r * v, axis=1, keepdims=True)) / mu
    ecc = np.sqrt((e ** 2).sum(axis=1, keepdims=True))
    if not (ecc == 1).any():
        sma = - mu / (2 * xi)
        p = sma * (1 - ecc ** 2)
    else:
        p = h_mag ** 2 / mu
        sma = p
    inc = np.arccos(h[:, 2, np.newaxis] / h_mag)
    node = np.arccos(n[:, 0, np.newaxis] / n_mag)
    if (n[:, 1] < 0).any():
        node[n[:, 1] < 0] = 2 * np.pi - node[n[:, 1] < 0]
    peri = np.arccos(np.sum(n * e, axis=1, keepdims=True) / (ecc * n_mag))
    if (e[:, 2] < 0).any():
        peri[e[:, 2] < 0] = 2 * np.pi - peri[e[:, 2] < 0]
    true_ano = np.arccos(np.sum(e * r, axis=1, keepdims=True) / (ecc * r_mag))
    if (np.sum(r * v, axis=1) < 0).any():
        true_ano[np.sum(r, v, axis=1) < 0] = 2 * np.pi - true_ano[np.sum(r * v, axis=1) < 0]
    if sma.shape == (1, 1):
        return np.hstack([sma, ecc, inc, node, peri, true_ano]).flatten()
    else:
        return np.hstack([sma, ecc, inc, node, peri, true_ano])


def vector(elements, mu):
    pass
