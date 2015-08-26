from __future__ import division, print_function
import numpy as np
import plyades.util as util

def precession(date):
    ''' Vallado 2nd Edition p.215
    '''
    # Julian centuries since the epoch
    t = (date - 2451545)/36525
    zeta = util.dms2rad(0, 0, 2306.2181*t + 0.30188*t**2 + 0.017998*t**3)
    theta = util.dms2rad(0, 0, 2004.3109*t - 0.42665*t**2 - 0.041833*t**3)
    z = util.dms2rad(0, 0, 2306.2181*t + 1.09468*t**2 + 0.018203*t**3)
    # Determine rotational matrices.
    M1 = util.rot(-z, axis=3)
    M2 = util.rot(theta, axis=2)
    M3 = util.rot(-zeta, axis=3)
    return np.dot(M1, np.dot(M2, M3))

# from scipy import optimize
#
# pvecle = aux.pvecle
# pelvec = aux.pelvec
#
#
# def eci2ecef(s, theta, omega):
#     M = np.zeros((6, 6))
#     M[0, 0] = np.cos(theta)
#     M[0, 1] = np.sin(theta)
#     M[1, 0] = -np.sin(theta)
#     M[1, 1] = np.cos(theta)
#     M[2, 2] = 1
#     M[3, 0] = -omega * np.sin(theta)
#     M[3, 1] = omega * np.cos(theta)
#     M[4, 0] = -omega * np.cos(theta)
#     M[4, 1] = -omega * np.sin(theta)
#     M[3, 3] = M[0, 0]
#     M[3, 4] = M[0, 1]
#     M[4, 3] = M[1, 0]
#     M[4, 4] = M[1, 1]
#     M[5, 5] = M[2, 2]
#
#     st = np.dot(M, s)
#     return st, M
#
# def ecef2eci(s, theta, omega):
#     M = np.zeros((3, 3))
#     N = np.zeros((3, 3))
#     st = np.zeros(6)
#     M[0, 0] = np.cos(theta)
#     M[0, 1] = np.sin(theta)
#     M[1, 0] = -np.sin(theta)
#     M[1, 1] = np.cos(theta)
#     M[2, 2] = 1
#     N[0, 0] = -omega * np.sin(theta)
#     N[0, 1] = omega * np.cos(theta)
#     N[1, 0] = -omega * np.cos(theta)
#     N[1, 1] = -omega * np.sin(theta)
#
#     st[0:3] = np.dot(M.T, s[0:3])
#     st[3:6] = np.dot(M.T, s[3:6]) + np.dot(N.T, s[0:3])
#     return st, M.T
#
#
#
# def lla2ecef(lat, lon, alt):
#     e = np.sqrt(2 * earth.f - earth.f ** 2)
#     c = earth.r_e / np.sqrt(1 - e ** 2 * np.sin(lat) ** 2)
#     s = c * (1 - e ** 2)
#     r_delta = (c + alt) * np.cos(lat)
#     r_k = (s + alt) * np.sin(lat)
#     return np.array([r_delta * np.cos(lon), r_delta * np.sin(lon), r_k])
#
#
# def ecef2lla(s, tol=1e-10):
#     x, y, z = s[0:3]
#     r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
#     r_delta = np.sqrt(x ** 2 + y ** 2)
#     lon = np.arctan2(y, x)
#
#     if abs(lon) >= np.pi:
#         if lon < 0:
#             lon = 2 * np.pi + lon
#         else:
#             lon = lon - 2 * np.pi
#
#     delta = np.arcsin(z / r)
#
#     def latitude(lat):
#         e = np.sqrt(2 * earth.f - earth.f ** 2)
#         c = earth.r_e / np.sqrt(1 - e ** 2 * np.sin(lat) ** 2)
#         return (z + c * e ** 2 * np.sin(lat)) / r_delta - np.tan(lat)
#
#     lat = optimize.newton(latitude, delta, tol=tol)
#
#     e = np.sqrt(2 * earth.f - earth.f ** 2)
#     c = earth.r_e / np.sqrt(1 - e ** 2 * np.sin(lat) ** 2)
#     alt = r_delta / np.cos(lat) - c
#
#     return np.array([lat, lon, alt])
#
#
# def ecef2sez(s, site=None, lat=None, lon=None, alt=None):
#     if not site == None:
#         ecef = site
#         lat, lon, alt = ecef2lla(ecef)
#     elif not lat == None or lon == None or alt == None:
#         ecef = lla2ecef(lat, lon, alt)
#     else:
#         raise SyntaxError("""Site location must be specified in
#             either ECEF format or lat/lon/alt!""")
#
#     rho_ecef = s[0:3] - ecef
#     rhod_ecef = s[3:6]
#
#     M = np.zeros((6, 6))
#     M[0, 0] = np.sin(lat) * np.cos(lon)
#     M[0, 1] = np.sin(lat) * np.sin(lon)
#     M[0, 2] = -np.cos(lat)
#     M[1, 0] = -np.sin(lon)
#     M[1, 1] = np.cos(lon)
#     M[2, 0] = np.cos(lat) * np.cos(lon)
#     M[2, 1] = np.cos(lat) * np.sin(lon)
#     M[2, 2] = np.sin(lat)
#     M[3:6, 3:6] = M[0:3, 0:3]
#
#     return np.dot(M, np.append(rho_ecef, rhod_ecef)), M
#
#
# def sez2razel(s):
#     ran = np.sqrt(np.dot(s[0:3], s[0:3]))
#     rrt = np.dot(s[0:3], s[3:6]) / ran
#     el = np.arcsin(s[2] / ran)
#     az = np.arctan2(s[1], -s[0])
#
#     return ran, rrt, az, el
#
