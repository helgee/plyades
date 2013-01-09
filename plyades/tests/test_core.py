from __future__ import division, print_function
import unittest
import plyades as pl

class EpochTest(unittest.TestCase):
	def setUp(self):
		self.epoch = pl.Epoch(2000,1,1,0,0,0)

	def test_jd(self):
		self.assertEqual(self.epoch.jd, pl.constants.EPOCH["JD2000"])

	def test_mjd2000(self):
		self.assertEqual(self.epoch.jd2000, 0)

	def test_mjd1950(self):
		self.assertEqual(self.epoch.jd1950, abs(pl.constants.EPOCH["JD1950"] - pl.constants.EPOCH["JD2000"]))

	def test_mjd(self):
		self.assertEqual(self.epoch.mjd, abs(pl.constants.EPOCH["MJD"] - pl.constants.EPOCH["JD2000"]))