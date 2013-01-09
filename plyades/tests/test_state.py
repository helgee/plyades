from __future__ import division, print_function
import unittest
import numpy as np
import plyades as pl

class StateTest(unittest.TestCase):
	def setUp(self):
		self.state = pl.State(np.array([1000, 1000, 1000, 1, 1, 1]))

	def test_s(self):
		self.assertTrue((self.state.s == np.array([1000, 1000, 1000, 1, 1, 1])).all())

	def test_r(self):
		self.assertTrue((self.state.r == 1000).all())

	def test_v(self):
		self.assertTrue((self.state.v == 1).all())
