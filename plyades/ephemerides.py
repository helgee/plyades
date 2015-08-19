from jplephem.spk import SPK
import networkx as nx
import numpy as np

class AnalyticalEphemeris:
    def __str__(self):
        return "Analytical Ephemeris."
    def rv(self, id, tdb, tdb2=0.0):
        raise NotImplementedError


class NumericalEphemeris:
    def __init__(self, spk):
        self.kernel = SPK.open(spk)
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
            return np.hstack(segment.compute_and_differentiate(tdb, tdb2))
        else:
            arr = np.zeros(6)
            for i1, i2 in zip(path, path[1:]):
                segment = self.kernel[i1, i2]
                arr += np.hstack(segment.compute_and_differentiate(tdb, tdb2))
            return arr
