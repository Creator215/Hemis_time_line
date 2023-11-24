import json

class Create_Json:
	def __init__(self,data):
		self.data = data

		self.key_ = ""
		self.val_1 = ""
		self.val_2 = ""

		self.for_json = ""
		self.new_json = ""
		self.for_json += "{"

		self.index = 0

		for i in self.data:
			if(self.index == 0):
				self.key_ = i
				self.for_json += """" """.replace(" ","") + self.key_ + """" """.replace(" ","") + ":" + "[" + """" """.replace(" ","")
				self.index = 1
			elif(self.index == 1):
				self.val_1 = i
				self.for_json += self.val_1 + """" """.replace(" ","") +"," + """" """.replace(" ","")
				self.index = 2
			elif(self.index == 2):
				self.val_2 = i
				self.for_json += self.val_2 + """" """.replace(" ","") + "],"
				self.index = 0
		self.for_json += "}"

		for k in range(len(self.for_json)):
			if(k == len(self.for_json)-2):
				pass
			else:
				self.new_json += self.for_json[k]

		self.j = json.loads(self.new_json)
		
	def get_json(self):
		return self.j
