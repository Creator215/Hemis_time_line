data = "56.  18 sentabr /  23 sentabr"


class Filter:
	def __init__(self,data):
		self.data = data

		self.filter_data_1 = ""
		self.filter_data_2 = ""
		nishon = "."
		nishon2 = "/"
		index = 0

		for i in self.data:
			if(i == nishon):
				index = 1
			if(index == 1):
				if(i != nishon2):
					self.filter_data_1 += i
				else:
					index = 2
			if(index == 2):
				self.filter_data_2 += i

	def get_sana_1(self):
		return self.filter_data_1.replace(".","").replace(" ","").replace("/","")
	def get_sana_2(self):
		return self.filter_data_2.replace(".","").replace(" ","").replace("/","")