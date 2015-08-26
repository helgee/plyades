from __future__ import division
import datetime
# from collections import namedtuple
import numpy as np
from plyades.constants import JD2000

def julian_centuries(jd, base=2451545.0):
    return (jd - base)/36525.0


def sidereal(jd):
    jd = np.atleast_1d(jd)
    t_ut1 = (jd - 2451545)/36525
    sidereal = (
                67310.54841 +
                (876600*3600 + 8640184.812866)*t_ut1 +
                .093104*t_ut1**2 - 6.2e-6*t_ut1**3)
    sidereal = np.remainder(np.radians(sidereal/240), 2*np.pi)
    if len(sidereal) == 1:
        return np.asscalar(sidereal)
    else:
        return sidereal


def calendar_jd(year, month, day, hour=0, minute=0, second=0, microsecond=0):
    year = np.atleast_1d(year)
    month = np.atleast_1d(month)
    day = np.atleast_1d(day)
    hour = np.atleast_1d(hour)
    minute = np.atleast_1d(minute)
    second = np.atleast_1d(second)
    microsecond = np.atleast_1d(microsecond)
    jd = (
        367 * year -
        np.floor((7 * (year + np.floor((month + 9) / 12.0))) * 0.25) +
        np.floor(275 * month / 9) +
        day + 1721013.5 +
        (((microsecond / 1e6 + second) / 60 + minute) / 60 + hour) / 24)
    if len(jd) == 1:
        return np.asscalar(jd)
    else:
        return jd


def datetime_jd(dt):
    try:
        years = [d.year for d in dt]
        months = [d.month for d in dt]
        days = [d.day for d in dt]
        hours = [d.hour for d in dt]
        minutes = [d.minute for d in dt]
        seconds = [d.second for d in dt]
        microseconds = [d.microsecond for d in dt]
    except TypeError:
        years = dt.year
        months = dt.month
        days = dt.day
        hours = dt.hour
        minutes = dt.minute
        seconds = dt.second
        microseconds = dt.microsecond
    return calendar_jd(
        years, months, days, hours, minutes, seconds, microseconds)


def jd_calendar(jd):
    jd = np.atleast_1d(jd) + .5
    z = np.trunc(jd)
    f = jd - z
    return f, z
    z_smaller = z < 2299161
    z_greater = z > 2299161
    a = np.zeros(jd.shape)
    alpha = np.zeros(jd.shape)
    if np.any(z_smaller):
        a[z_smaller] = z[z_smaller]
    if np.any(z_greater):
        alpha[z_greater] = np.trunc((z[z_greater] - 1867216.25)/36524.25)
        a[z_greater] = z[z_greater] + 1 + alpha - np.trunc(alpha/4)
    b = a + 1524
    c = np.trunc((b - 122.1)/365.25)
    d = np.trunc(365.25*c)
    e = np.trunc((b - d)/30.6001)
    day = np.floor(b - d - np.trunc(30.6001*e) + f)
    day = day.astype(np.int64, copy=False)
    e_smaller = e < 14
    e_greater = e > 14
    month = np.zeros(jd.shape, dtype=np.int64)
    if np.any(e_smaller):
        month[e_smaller] = e[e_smaller] - 1
    if np.any(e_greater):
        month[e_greater] = e[e_greater] - 13
    month_smaller = month > 2
    month_greater = month < 2
    year = np.zeros(jd.shape, dtype=np.int64)
    if np.any(month_smaller):
        year[month_smaller] = c[month_smaller] - 4716
    if np.any(month_greater):
        year[month_greater] = c[month_greater] - 4715
    hours = f*24
    hour = np.floor(hours).astype(np.int64, copy=False)
    minutes = (hours - hour) * 60
    minute = np.floor(minutes).astype(np.int64, copy=False)
    seconds = (minutes - minute) * 60
    second = np.floor(seconds).astype(np.int64, copy=False)
    microsecond = ((seconds - second) * 1e6).astype(np.int64, copy=False)
    # t = f*86400
    # hmod = np.mod(t, 3600)
    # second = np.mod(hmod, 60)
    # hour = np.trunc((t - hmod)/3600)
    # hour = hour.astype(np.int64, copy=False)
    # minute = np.trunc((hmod - second)/60)
    # minute = minute.astype(np.int64, copy=False)
    if len(year) == 1:
        return (np.asscalar(year),
                np.asscalar(month),
                np.asscalar(day),
                np.asscalar(hour),
                np.asscalar(minute),
                np.asscalar(second),
                np.asscalar(microsecond),
                )
    else:
        return year, month, day, hour, minute, second, microsecond


def jd_datetime(jd):
    jd = np.atleast_1d(jd)
    cal = jd_calendar(jd)
    try:
        return [
            datetime.datetime(
                year, month, day, hour, minute, second, microsecond)
            for year, month, day, hour, minute, second, microsecond in cal]
    except TypeError:
        return datetime.datetime(*cal)
