import datetime
import numpy as np
import constants

class Epoch(datetime.datetime):
	@property
	def jd(self):
		return datetime2jd(self)

	@property
	def jd2000(self):
		return self.jd - constants.EPOCH["JD2000"]

	@property
	def jd1950(self):
		return self.jd - constants.EPOCH["JD1950"]

	@property
	def mjd(self):
		return self.jd - constants.EPOCH["MJD"]

def datetime2jd(dt):
	return (367.0 * dt.year
			 - np.floor( (7 * (dt.year + np.floor( (dt.month + 9) / 12.0) ) ) * 0.25 )
             + np.floor( 275 * dt.month / 9.0 )
             + dt.day + 1721013.5
             + ( (dt.second/60.0 + dt.minute ) / 60.0 + dt.hour ) / 24.0)