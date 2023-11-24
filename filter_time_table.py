class Filter_Time_Table:
	def __init__(self,data):

		self.data = data
		self.week_data = []
		self.day_time = []
		self.Time = []
		self.day_room = []
		self.Room = []
		self.type_ = []
		self.Type = []
		self.t_name = []
		self.Name_ = []
		self.demo_name = []
		self.science_name = []
		self.science = []
		self.list_value_help = []
		self.list_value_ = []
		self.list_value = []
		self.json_d = ""


		self.week_days = ["Dushanba","Seshanba","Chorshanba","Payshanba","Juma","Shanba"]

		z = (self.data.find_all("div",class_ = "box-header with-border"))

		time = (self.data.find_all("ul",class_ = "nav nav-stacked"))


		for k in z:

			ff = (k.find("span").text.replace("\t","").replace(" ","").replace("\r","").replace("\n",""))
			dd = (k.text.replace("\t","").replace(" ","").replace("\r","").replace("\n","").replace(ff,""))
			self.week_data.append(dd)

		#print(self.week_data) -- OK

		for kk in time:
			tt = (kk.find_all("span",class_ = "pull-right text-muted"))
			for f in tt:
				self.day_time.append(f.text)
			self.Time.append(self.day_time)
			self.day_time = []

		for nn in time:

			p = (nn.find_all("span",class_ = "text-center text-muted"))
			zz = (nn.find_all("li",class_ = "list-group-item"))

			for pp in range(0,len(p),3):

				self.day_room.append(p[pp].text)
				self.type_.append(p[pp+1].text)
				self.t_name.append(p[pp+2].text)

			self.Room.append(self.day_room)
			self.Type.append(self.type_)
			self.Name_.append(self.t_name)
			self.day_room = []
			self.type_ = []
			self.t_name = []

			for names in zz:
				self.demo_name.append(names.text.replace("\t","").replace("  ","").replace("\r","").replace("\n",""))

		#print(self.Name_) -- Ok
		#print(self.Type) -- Ok
		#print(self.Room) -- Ok
		#print(self.Time) -- OK
		ind = 0
		ind2 = 0
		for i in (self.Name_):
			for j in range(len(i)):
				for_replace = (self.Room[ind][j] + "/" + self.Type[ind][j] + "/" + self.Name_[ind][j] + self.Time[ind][j])
				self.science_name.append(self.demo_name[ind2].replace(for_replace,"")[3:])
				ind2 += 1
			ind += 1
			self.science.append(self.science_name)
			self.science_name = []

		#print(self.science) -- Ok

		for lists in range(len(self.science)):
			for index2 in range(len(self.science[lists])):
				self.list_value_help.append(self.Time[lists][index2])
				self.list_value_help.append(self.science[lists][index2])
				self.list_value_help.append(self.Room[lists][index2])
				self.list_value_help.append(self.Type[lists][index2])
				self.list_value_help.append(self.Name_[lists][index2])
				self.list_value_.append(self.list_value_help)
				self.list_value_help = []
			self.list_value.append(self.list_value_)
			self.list_value_ = []
		iid = 0
		for_ = ""
		for_ += "{"
		for kkk in self.list_value:
			#print(kkk)

			for_ += ("\"" + self.week_days[iid] + "\"" + ":" + str(kkk) + ",").replace("\'", "\"")
			iid += 1
			pass
		for_ += "}"

		for index_x in range(len(for_)):
			if(index_x == len(for_)-2):
				pass
			else:
				self.json_d += for_[index_x]
		#print(self.json_d) -- Ok

	def get_data(self):
		return self.json_d