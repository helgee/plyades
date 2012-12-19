import numpy as np

class State:
	def __init__(self, x, y, z, vx, vy, vz, epoch=Epoch(2000,1,1,0,0,0), frame="MEE2000"):
		self.r = np.array([x, y, z])
		self.v = np.array([vx, vy, vz])
		self.t = epoch