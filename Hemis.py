import requests
from bs4 import BeautifulSoup
from filter_ import Filter
from create_json import Create_Json
from date_Decoder import Date_Decoder
from filter_time_table import Filter_Time_Table
import json


class Hemis:
	def  __init__(self,user_login,user_password,my_day,my_date):
		
		self.user_login = user_login
		self.user_password = user_password
		self.my_day = my_day
		self.my_date = my_date

		self.identification_url = "https://student.tatunf.uz/student/personal-data"
		self.time_tabel_url = "https://student.tatunf.uz/education/time-table"
		self.get_time_table_data_url = ""
		self.json_data = None
		self.json_data2 = None
		self.ss_data = []

		with requests.session() as sessiya:
			begin_request = sessiya.request("GET",url = self.identification_url)
			for_filters = BeautifulSoup(begin_request.text,"html.parser")

			csrf_token = for_filters.find_all("meta")[4]["content"]

			send_data = {
				"FormStudentLogin[login]" : self.user_login,
				"FormStudentLogin[password]" : self.user_password,
				"_csrf-frontend" : csrf_token
			}

			end_request = sessiya.request("POST",url = begin_request.url,data = send_data,timeout = 5000)
			filters_ = BeautifulSoup(end_request.text,"html.parser")

			get_semester = filters_.find_all("table",id = "w4")
			sample_data_key = ""
			sample_data_value = ""
			for_json = ""
			index = 0
			for_json += "{"
			for i in (get_semester[0].find_all("tr")):
				sample_data_key = (i.find("th").text)
				sample_data_value = (i.find("td").text)
				for_json += """" """.replace(" ","") + sample_data_key + """" """.replace(" ","") + ":" + """" """.replace(" ","") + sample_data_value + """" """.replace(" ","") + ","

			for_json += "}"
			sizes = len(for_json)
			new_json = ""

			for ins in range(sizes):

				if(ins == sizes-2):
					pass
				else:
					new_json += for_json[ins]

			self.json_data = json.loads(new_json)

			sessiya.close()

		with requests.session() as sses:
			for_time_table_begin_request = sses.request("GET",url = self.time_tabel_url)
			for_time_table_begin_request_filter = BeautifulSoup(for_time_table_begin_request.text,"html.parser")

			time_table_csrf_token = for_time_table_begin_request_filter.find_all("meta")[4]["content"]

			sending_data = {
				"FormStudentLogin[login]" : self.user_login,
				"FormStudentLogin[password]" : self.user_password,
				"_csrf-frontend" : time_table_csrf_token
			}


			get_time_data_html = sses.request("POST",url = for_time_table_begin_request.url,data = sending_data,timeout=5000)

			bss = BeautifulSoup(get_time_data_html.text,"html.parser")
			k = bss.find_all("option")

			for i in k:
				if((i.text != "") and (i["value"] != "")):
					self.ss_data.append(i["value"])
					self.ss_data.append(Filter(i.text).get_sana_1())
					self.ss_data.append(Filter(i.text).get_sana_2())
			
			


	def get_identification_data(self):
		return self.json_data


	def get_time_table_data_json(self):

		x = Create_Json(self.ss_data)
		y = (x.get_json())
		z = Date_Decoder(y)
		link = ""
		for i in range(len(z.get_data())):
			if(z.get_data()[i][1] == self.my_date):
				if(z.get_data()[i][0] >= self.my_day):
					link = (list(y)[int(i/2)])
					break


		with requests.session() as sss:
			l_link = f"https://student.tatunf.uz/education/time-table?week={link}"
			b_connection = sss.request("GET",url = l_link)
			filter_tocen = BeautifulSoup(b_connection.text,"html.parser")

			c_token = filter_tocen.find_all("meta")[4]["content"]

			s_data = {
				"FormStudentLogin[login]" : self.user_login,
				"FormStudentLogin[password]" : self.user_password,
				"_csrf-frontend" : c_token
			}
			
			p_request = sss.request("POST",data = s_data,url = b_connection.url,timeout = 5000)

			f_data = BeautifulSoup(p_request.text,"html.parser")

			filter_ddd = Filter_Time_Table(f_data)
			XYZ = filter_ddd.get_data()
			#JJJ = json.loads(XYZ)
			_data = """{"Dushanba":[["12","11","10"],["12","10","8"],["8","7","3"]],"Seshanba":[["12","11","10"],["12","10","8"],["8","7","3"]]}"""

		return json.loads(XYZ)