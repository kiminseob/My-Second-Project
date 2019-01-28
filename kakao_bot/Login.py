#import requests
import sys
sys.path.insert(0,'/usr/local/lib/python3.5/dist-packages')
import requests
from bs4 import BeautifulSoup as bs
import re
import datetime,time
from myHome.inseopbot import Name
from myHome.inseopbot import test_bot
from multiprocessing import Process

my_name=""
my_major=""

LOGIN_INFO = {
    #login info
}

# login to the cyber campus.
def login(input_id,state,userID):
	with requests.Session() as s:
		global my_name,my_major

		id = input_id.split("/")[0]
		pw = input_id.split("/")[1]

		LOGIN_INFO['user_id'] = id
		LOGIN_INFO['user_password'] = pw
		req = s.post('http://e-learn.cnu.ac.kr/login/doGetUserCountId.dunet', data=LOGIN_INFO)

		try:
			data = req.json()
			print(data["MSG"])
			if data['MSG']=="아이디 또는 패스워드정보가 잘못됐습니다.":
				print("로그인실패")
				return False
			else:
				print("로그인성공")
		except KeyError as e:
			print(e)

		req = s.get('http://e-learn.cnu.ac.kr/main/MainView.dunet')
		soup = bs(req.text, 'html.parser')
		p = re.compile("user_name = '\w*'")
		p2 = re.compile("deptGroup = '\w*'")
		m = p.findall(soup.text)
		m2 = p2.findall(soup.text)

		if state:
			my_name = m.__getitem__(0).split("'")[1]
			my_major = m2.__getitem__(0).split("'")[1]
		if not state:
			proc = Process(target=CrawlingBot.main,args=(input_id,userID,s))
			proc.start()
		return True
		


	