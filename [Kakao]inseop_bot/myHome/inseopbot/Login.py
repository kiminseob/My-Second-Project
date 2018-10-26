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
'''
LOGIN_INFO = {
    'user_id':ID,
    'user_password': PW,
    'is_local':'Y',
    'group_cd':'UN',
    'sub_group_cd': ''
}
LOGIN_INFO_2 = {
    'user_id':"",
    'user_password':"",
    'user_ip': "",
    'group_cd':'UN',
    'sub_group_cd': ''
}'''
LOGIN_INFO_2 = {
    'user_id':"",
    'user_password':"",
	'is_local':"Y",
    'group_cd':'UN',
	'user_ip': "",
    'sub_group_cd': ''
}

def login(input_id,state,userID): #사이버캠퍼스에 로그인
	with requests.Session() as s:
		global my_name,my_major
		'''
		global post_ip,post_pw,ID,PW
		ID = input_id
		#로그인 폼 전송1
		for key in LOGIN_INFO.keys():
			if key == "user_id":
				LOGIN_INFO[key] = ID
			if key == "user_password":
				LOGIN_INFO[key] = PW
		req = s.post('http://e-learn.cnu.ac.kr/login/doGetUserCountId.dunet', data=LOGIN_INFO)
		try:
			#폼 비번
			splited_pw = req.text.split('user_password":"')
			post_pw= splited_pw[1].split('"')
		except IndexError as e:
			return False
		'''
		id = input_id.split("/")[0]
		pw = input_id.split("/")[1]
		LOGIN_INFO_2['user_id'] = id
		LOGIN_INFO_2['user_password'] = pw
		req = s.post('http://e-learn.cnu.ac.kr/login/doGetUserCountId.dunet', data=LOGIN_INFO_2)
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
		p = re.compile("user_name = '\w*'")  ##정규포현식 사용
		p2 = re.compile("deptGroup = '\w*'")
		m = p.findall(soup.text)
		m2 = p2.findall(soup.text)

		if state:
			my_name = m.__getitem__(0).split("'")[1] #이름
			my_major = m2.__getitem__(0).split("'")[1] #학과
		if not state:
			proc = Process(target=test_bot.main,args=(input_id,userID,s))
			proc.start()
		return True
		


	