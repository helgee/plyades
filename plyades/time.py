import datetime
import numpy as np
import constants

class Epoch(datetime.datetime):
	@property
	def jd(self):
		jd = (367.0 * self.year
			 - np.floor( (7 * (self.year + np.floor( (self.month + 9) / 12.0) ) ) * 0.25 )
             + np.floor( 275 * self.month / 9.0 )
             + self.day + 1721013.5
             + ( (self.second/60.0 + self.minute ) / 60.0 + self.hour ) / 24.0)
		return jd

	@property
	def jd2000(self):
		return self.jd - constants.EPOCH["MJD2000"]

	@property
	def jd1950(self):
		return self.jd - constants.EPOCH["MJD1950"]

	@property
	def mjd(self):
		return self.jd - constants.EPOCH["MJD"]