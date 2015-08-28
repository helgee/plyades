"""`plyades.util` contains mathematical and miscellaneous utility functions.
"""
from __future__ import division
import re
import numpy as np
import astropy.units as u

def istime(t):
    try:
        t.jd
    except AttributeError:
        return False
    else:
        return True

def nearest_idx(array, value):
    return (np.abs(array-value)).argmin()

def rot(angle, axis=3):
    '''

    '''
    M = np.zeros((3,3))
    if axis == 1:
        M[0,0] = 1
        M[1,1] = np.cos(angle)
        M[1,2] = np.sin(angle)
        M[2,1] = -np.sin(angle)
        M[2,2] = np.cos(angle)
        return M
    elif axis == 2:
        M[0,0] = np.cos(angle)
        M[0,2] = -np.sin(angle)
        M[1,1] = 1
        M[2,0] = np.sin(angle)
        M[2,2] = np.cos(angle)
        return M
    elif axis == 3:
        M[0,0] = np.cos(angle)
        M[0,1] = np.sin(angle)
        M[1,0] = -np.sin(angle)
        M[1,1] = np.cos(angle)
        M[2,2] = 1
        return M

def rotd(angle, angular_velocity, axis=3):
    M = np.zeros((3,3))
    if axis == 1:
        M[1,1] = -angular_velocity * np.sin(angle)
        M[1,2] = angular_velocity * np.cos(angle)
        M[2,1] = -angular_velocity * np.cos(angle)
        M[2,2] = -angular_velocity * np.sin(angle)
        return M
    elif axis == 2:
        M[0,0] = -angular_velocity * np.sin(angle)
        M[0,2] = -angular_velocity * np.cos(angle)
        M[2,0] = angular_velocity * np.cos(angle)
        M[2,2] = -angular_velocity * np.sin(angle)
        return M
    elif axis == 3:
        M[0,0] = -angular_velocity * np.sin(angle)
        M[0,1] = angular_velocity * np.cos(angle)
        M[1,0] = -angular_velocity * np.cos(angle)
        M[1,1] = -angular_velocity * np.sin(angle)
        return M

def euler(alpha, beta, gamma, order="321"):

    # Input checking.
    reg = re.compile("[1-3][1-3][1-3]")
    if not reg.match(order) and len(order) > 3:
        raise ValueError("Incorrect rotation order definition.")

    m_alpha = rot(alpha, axis=int(order[0]))
    m_beta = rot(beta, axis=int(order[1]))
    m_gamma = rot(gamma, axis=int(order[2]))
    return np.dot(m_alpha, np.dot(m_beta, m_gamma))

def dms2rad(degrees, minutes, seconds):
    return (degrees + minutes/60 + seconds/3600) * np.pi/180

def hms2rad(degrees, minutes, seconds):
    return (degrees + minutes/60 + seconds/3600) * 15 * np.pi/180

def mag(a):
    """Vectorized magnitude calculation for an array of vectors.

    Parameters
    ----------
    a: numpy.ndarray
        An mxn-array containing m vectors with n elements.

    Returns
    -------
    m: numpy.ndarray
        An mx1-array containing the magnitude for each vector.
    """
    return np.sqrt(np.square(a).sum(axis=1, keepdims=True))

def dot(a, b):
    """Vectorized dot product for arrays of vectors.

    Parameters
    ----------
    a: numpy.ndarray
        An mxn-array containing m vectors with n elements.
    b: numpy.ndarray
        An mxn-array containing m vectors with n elements.


    Returns
    -------
    m: numpy.ndarray
        An mx1-array containing of a*b for each vector pair.
    """
    return (a * b).sum(axis=1, keepdims=True)

def getunit(val):
    return getattr(val, "unit", None)

def cross(a, b):
    unit_a = getunit(a)
    unit_b = getunit(b)
    if not unit_a and not unit_b:
        return np.cross(a, b)
    else:
        if not unit_a:
            unit_a = u.dimensionless_unscaled
        if not unit_b:
            unit_b = u.dimensionless_unscaled
        return np.cross(a, b)*unit_a*unit_b


def mod2pi(val):
    unit = getunit(val)
    if not unit:
        return np.mod(val, 2*np.pi)
    else:
        return np.mod(val, 2*np.pi*unit)
