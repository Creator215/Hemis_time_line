
class Date_Decoder:
	def __init__(self,data):
		self.data = data

		self.date_list = {
				"yanvar":1,
				"fevral":2,
				"mart":3,
				"aprel":4,
				"may":5,
				"iyun":6,
				"iyul":7,
				"avgust":8,
				"sentabr":9,
				"oktabr":10,
				"noyabr":11,
				"dekabr":12
			}
		self.numbers = ["0","1","2","3","4","5","6","7","8","9"]
		self.kun = ""
		self.sana = ""
		self.mass = []
		self.mass2 = []
		self.mass_help = []
		self.mass_help2 = []
		for i in self.data:
			for k in self.data[i][0]:
				for t in self.numbers:
					if(k == t):
						self.kun += k
					else:
						pass

			self.mass.append(int(self.kun))
			self.sana = self.data[i][0].replace(self.kun,"")
			self.mass.append(self.date_list[self.sana])
			self.kun = ""



			for u in self.data[i][1]:
				for v in self.numbers:
					if(u == v):
						self.kun += u
					else:
						pass

			self.mass.append(int(self.kun))
			self.sana = self.data[i][1].replace(self.kun,"")
			self.mass.append(self.date_list[self.sana])
			self.kun = ""

		for i in range(0,int(len(self.mass)),2):

			self.mass_help.append(self.mass[i])
			self.mass_help.append(self.mass[(i + 1)])
			self.mass2.append(self.mass_help)
			self.mass_help = []

	
	def get_data(self):
		#print(self.mass2)
		return self.mass2