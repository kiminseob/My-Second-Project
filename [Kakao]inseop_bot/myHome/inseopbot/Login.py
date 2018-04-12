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

post_ip = [0 for _ in range(2)]#post 전송 시 ip
post_pw = [0 for _ in range(2)]#post 전송 시 pw
ID="" #아이디
PW="" #비번
my_name=""

LOGIN_INFO = {
   "로그인폼1"
}
LOGIN_INFO_2 = {
   "로그인폼2"
}
def login(input_id,state,userID): #이러닝 캠퍼스 사이트에 로그인
	with requests.Session() as s:
		global post_ip,post_pw,ID,PW
		ID = input_id
		#로그인 폼 전송1
		for key in LOGIN_INFO.keys():
			if key == "user_id":
				LOGIN_INFO[key] = ID
			if key == "user_password":
				LOGIN_INFO[key] = PW
		req = s.post('로그인 페이지 주소', data=LOGIN_INFO)
		try:
			#폼 비번
			splited_pw = req.text.split('user_password":"')
			post_pw= splited_pw[1].split('"')
		except IndexError as e:
			return False
		
		#폼 아이피주소
		splited_ip = req.text.split('client_ip":"')
		post_ip = splited_ip[1].split('"')
		#로그인 폼 전송2
		for key in LOGIN_INFO_2.keys():
			if key == "user_id":
				LOGIN_INFO_2[key] = ID
		s.post('로그인 페이지 주소', data=LOGIN_INFO_2)
		print("로그인성공")
		if state:
			Name.my_name_fuc(s)
		if not state:
			proc = Process(target=test_bot.main,args=(input_id,userID,s))
			proc.start()
		return True
		


	