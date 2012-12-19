import datetime
import numpy as np

class Epoch(datetime.datetime):
	def get_jd(self, epoch=2000):
		jd = (367.0 * self.year
			 - np.floor( (7 * (self.year + np.floor( (self.month + 9) / 12.0) ) ) * 0.25 )
             + np.floor( 275 * self.month / 9.0 )
             + self.day + 1721013.5
             + ( (self.second/60.0 + self.minute ) / 60.0 + self.hour ) / 24.0)
		if epoch == 2000:
			return jd - 2451544.5
		elif epoch == 1950:
			return jd - 2433282.5
		elif epoch == "mjd":
			return jd - 2400000.5
		elif epoch == 0:
			return jd

class State:
	def __init__(self, x, y, z, vx, vy, vz, epoch=Epoch(2000,1,1,0,0,0)):
		self.r = np.array([x, y, z])
		self.v = np.array([vx, vy, vz])
		self.t = epoch