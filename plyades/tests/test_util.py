from __future__ import division, print_function
import unittest
import numpy as np
import plyades as pl

class UtilTest(unittest.TestCase):
	def test_dms(self):
		self.assertEqual(pl.util.dms2rad(1,0,0), np.radians(1))
		self.assertEqual(pl.util.dms2rad(0,1,0), np.radians(1)/60)
		self.assertEqual(pl.util.dms2rad(0,0,1), np.radians(1)/3600)

	def test_hms(self):
		self.assertEqual(pl.util.hms2rad(1,0,0), np.radians(15))
		self.assertEqual(pl.util.hms2rad(0,1,0), np.radians(15)/60)
		self.assertEqual(pl.util.hms2rad(0,0,1), np.radians(15)/3600)