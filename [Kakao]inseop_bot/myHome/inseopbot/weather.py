from bs4 import BeautifulSoup as bs
import sys
sys.path.insert(0,'/usr/local/lib/python3.5/dist-packages')
import requests

todayTemp=""
compareTemp=""
#fineDust=""

def find_weather():
	global todayTemp,compareTemp
	headers = {'Accept-Encoding': None}
	URL = "https://search.naver.com/search.naver"
	params={
		'ie': 'UTF-8',
		'sm': 'chr_hty',
		'query' : '대전 궁동 날씨'
	}
	naver_weather_html = requests.get(URL,headers=headers, params=params)
	soup = bs(naver_weather_html.text, "html.parser")
	todayTemp = soup.find("span", {"class": "todaytemp"}).text# 유성구 궁동의 현재온도
	compareTemp = soup.find("p", {"class": "cast_txt"}).text  # 어제의 날씨와 비교한 온도 설명
	#fineDust = soup.find("dd", {"class": "lv2"}).text  # 미세먼지 농도

