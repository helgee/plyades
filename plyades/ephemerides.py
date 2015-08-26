from jplephem.spk import SPK
import networkx as nx
import numpy as np

class AnalyticalEphemeris:
    def __str__(self):
        return "Analytical Ephemeris."
    def rv(self, id, tdb, tdb2=0.0):
        raise NotImplementedError


class NumericalEphemeris:
    def __init__(self, spk, units):
        self.kernel = SPK.open(spk)
        self.r_unit = units[0]
        self.v_unit = units[1]
        self.graph = nx.Graph()
        for edge in self.kernel.pairs:
            self.graph.add_edge(*edge)
        self.paths = nx.shortest_path(self.graph)
    def __str__(self):
        return str(self.kernel)
    def rv(self, id, tdb, tdb2=0.0):
        if id not in self.graph:
            raise ValueError("Unknown body ID: {}".format(id))
        path = self.paths[0][id]
        if len(path) == 2:
            segment = self.kernel[0, id]
            r, v = segment.compute_and_differentiate(tdb, tdb2)
        else:
            r = np.zeros(3)
            v = np.zeros(3)
            for i1, i2 in zip(path, path[1:]):
                segment = self.kernel[i1, i2]
                rs, vs = segment.compute_and_differentiate(tdb, tdb2)
                r += rs
                v += vs
        return r * self.r_unit, v * self.v_unit
