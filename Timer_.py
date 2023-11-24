class Timer_:
	def __init__(self,time_,interval):
		self.time_ = time_
		self.interval = interval

		self.soat = int(self.time_[:2])
		self.daqiqa = int(time_[3:])
		self.soat_ = None
		self.daqiqa_ = None
		self.kirish = ""
		
		if(self.daqiqa < self.interval):
			self.daqiqa_ = 60 - (self.interval-self.daqiqa)
			self.soat_ = self.soat - 1
			if(self.daqiqa_ == 0):
				if(len(str(self.soat_)) == 1):
					self.kirish += f"0{self.soat_}" + ":00"
				else:
					self.kirish += str(self.soat_) + ":00"
			else:
				self.kirish += str(self.soat_) + ":" + str(self.daqiqa_)
		else:
			self.daqiqa_ = self.daqiqa - self.interval
			self.soat_ = self.soat
			if(self.daqiqa_ == 0):
				if(len(str(self.soat_)) == 1):
					self.kirish += f"0{self.soat_}" + ":00"
				else:
					self.kirish += str(self.soat_) + ":00"
			else:

				self.kirish += str(self.soat_) + ":" + str(self.daqiqa_)

		
	def get_new_time(self):
		return self.kirish