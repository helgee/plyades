from __future__ import division, print_function
import unittest
import datetime
import numpy as np
import plyades as pl


class StateTest(unittest.TestCase):
    def setUp(self):
        self.state = pl.State(np.array([1000,1000,1000,1,1,1]),t=datetime.datetime(2000, 1, 1, 0, 0, 0))

    def test_jd(self):
        self.assertEqual(self.state.jd, pl.const.epoch["jd2000"])

    def test_mjd2000(self):
        self.assertEqual(self.state.jd2000, 0)

    def test_mjd1950(self):
        self.assertEqual(self.state.jd1950, abs(pl.const.epoch["jd1950"] - pl.const.epoch["jd2000"]))

    def test_mjd(self):
        self.assertEqual(self.state.mjd, abs(pl.const.epoch["mjd"] - pl.const.epoch["jd2000"]))
