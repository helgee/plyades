from __future__ import division, print_function
import unittest
import numpy as np
import plyades as pl


values = {"vector": np.array([6524.834, 6862.875, 6448.296, 4.901327, 5.533756, -1.976341]),
          "elements": np.array([36127.343, 0.832853, np.radians(87.870), np.radians(227.89),
                                np.radians(53.38), np.radians(92.335)])}


class OrbitTest(unittest.TestCase):
    def test_elements(self):
        elements = pl.orbit.elements(values["vector"], pl.constants.earth.mu)
        for i in range(len(elements)):
            self.assertAlmostEqual(elements[i], values["elements"][i], delta=1e-2)

    def test_elements_vectorized(self):
        elements = pl.orbit.elements(np.vstack((values["vector"], values["vector"])), pl.constants.earth.mu)
        for el in elements:
            for i in range(len(el)):
                self.assertAlmostEqual(el[i], values["elements"][i], delta=1e-2)

    def test_vector(self):
        vector = pl.orbit.vector(values["elements"], pl.constants.earth.mu)
        for i in range(len(vector)):
            self.assertAlmostEqual(vector[i], values["vector"][i], delta=1e-2)

    def test_vector_vectorized(self):
        vector = pl.orbit.vector(np.vstack((values["elements"], values["elements"])), pl.constants.earth.mu)
        for v in vector:
            for i in range(len(v)):
                self.assertAlmostEqual(v[i], values["vector"][i], delta=1e-2)
