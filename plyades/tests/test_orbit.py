from __future__ import division, print_function
import unittest
import numpy as np
import plyades as pl


VALUES = {"vector": np.array([6524.834, 6862.875, 6448.296, 4.901327, 5.533756, -1.976341]),
          "elements": np.array([36127.343, 0.832853, np.radians(87.870), np.radians(227.89),
                                np.radians(53.38), np.radians(92.335)])}


class OrbitTest(unittest.TestCase):
    def test_elements(self):
        elements = pl.orbit.elements(VALUES["vector"], pl.const.EARTH["mu"])
        for i in range(len(elements)):
            self.assertAlmostEqual(elements[i], VALUES["elements"][i], delta=1e-2)

    def test_elements_vectorized(self):
        elements = pl.orbit.elements(np.vstack((VALUES["vector"], VALUES["vector"])), pl.const.EARTH["mu"])
        for el in elements:
            for i in range(len(el)):
                self.assertAlmostEqual(el[i], VALUES["elements"][i], delta=1e-2)


    # def test_vector(self):
    #     self.assertAlmostEqual(pl.orbit.vector(VALUES["elements"], pl.const.EARTH['mu']), VALUES["vector"])

    # def test_vector_vectorized(self):
    #     self.assertAlmostEqual(pl.orbit.vector(np.vstack((VALUES["elements"], VALUES["elements"])), pl.const.EARTH['mu']), np.vstack((VALUES["vector"], VALUES["vector"])))
