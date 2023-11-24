import requests

class Uzb_time_zona:
    def __init__(self):

        self.message = ""
        self.my_region_url = "https://www.timeapi.io/api/Time/current/zone?timeZone=Asia/Tashkent"
        self.lists = {}
        try:
            self.session = requests.Session()
            self.get_request = self.session.get(url = self.my_region_url).json()
            self.message = ""
        except:
            self.message = "connect_error"

    def vaqt(self,value):
        if(self.message != "connect_error"):
            if(value == "soat"):
                return int(self.get_request["hour"])
            elif(value == "daqiqa"):
                return int(self.get_request["minute"])
        else:
            return -1

    def sana(self,value):
        if(self.message != "connect_error"):
            if(value == "oy"):
                return int(self.get_request["month"])
            elif(value == "kun"):
                return int(self.get_request["day"])
        else:
            return -1

    def hafta(self):

        if(self.message != "connect_error"):
            week_name = ""
            z = self.get_request["dayOfWeek"]
    
            if(z == "Monday"):
                week_name = "Dushanba"
            elif(z == "Tuesday"):
                week_name = "Seshanba"
            elif(z == "Wednesday"):
                week_name = "Chorshanba"
            elif(z == "Thursday"):
                week_name = "Payshanba"
            elif(z == "Friday"):
                week_name = "Juma"
            elif(z == "Saturday"):
                week_name = "Shanba"
            else:
                week_name = "Yakshanba"
            return week_name

    def hafta2(self):

        if (self.message != "connect_error"):
            week_name = ""
            z = self.get_request["dayOfWeek"]

            if (z == "Monday"):
                week_name = "Seshanba"
            elif (z == "Tuesday"):
                week_name = "Chorshanba"
            elif (z == "Wednesday"):
                week_name = "Payshanba"
            elif (z == "Thursday"):
                week_name = "Juma"
            elif (z == "Friday"):
                week_name = "Shanba"
            elif (z == "Saturday"):
                week_name = "Yakshanba"
            else:
                week_name = "Dushanba"
            return week_name