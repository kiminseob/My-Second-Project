#import requests
import sys
sys.path.insert(0,'/usr/local/lib/python3.5/dist-packages')
import requests
from bs4 import BeautifulSoup as bs
import re
import datetime,time
from datetime import datetime

from myHome.models import MY_HOME
from myHome.inseopbot import Announcement
from myHome.inseopbot import Homework
from myHome.inseopbot import Resource

my_course_id = [] #과목번호
my_class_no = [] #과목분반
my_corse_name = [] #과목이름
my_corse_num =0 #수강 과목 갯수

my_all_resource=""
my_all_homework=""
my_all_announcement=""

MY_CLASS_FORM={
    'class_no':"",
    'course_id':"",
    'mnid':  "201008254671"
}
MY_RESOURCE_FORM={
    'mnid':"20100863099",
    'board_no':'6'
}

def my_course_fuc(s): ##강의실 ID 파싱
	global my_corse_num,my_corse_name,my_course_id,my_class_no
	my_page = s.get('http://e-learn.cnu.ac.kr/lms/myLecture/doListView.dunet?mnid=201008840728')  # 강의목록확인
	soup = bs(my_page.text, 'html.parser')
	temp = soup.findAll("a", {"class": "classin2"})
	count = temp.__len__()
	my_corse_num = count
	temp2 = temp.__str__()

	p = re.compile('course.id..\w{23}.')  ##정규포현식 사용
	p2 = re.compile('class_no..\d\d')
	m = p.findall(temp2)
	m2 = p2.findall(temp2)

	name_splited_temp = temp2.split("<br/>")

	# 과목번호, 분반, 과목명을 추출한다.
	for i in range(count):
		my_course_id.append(m[i].split('"')[1])
		my_class_no.append(m2[i].split('"')[1])
		my_corse_name.append(name_splited_temp[i].split('"">')[1].strip())

def my_all_list(s): #공지,자료실,과제 리스트 모두 가져온다
	global my_all_announcement,my_all_homework,my_all_resource
	procs=[] # 프로세스들
	# 모든 강의실 접속해서 과제,공지,자료실 내용 가져오기
	for i in range(my_corse_num):
		MY_CLASS_FORM['class_no'] = my_class_no[i]
		MY_CLASS_FORM['course_id'] = my_course_id[i]
		homework_page = s.post('http://e-learn.cnu.ac.kr/lms/class/classroom/doViewClassRoom_new.dunet', data=MY_CLASS_FORM)
		# 특정 강의홈 입장
		#homework_page = s.get('http://e-learn.cnu.ac.kr/lms/class/classroom/doViewClassRoom_new.dunet')
		soup = bs(homework_page.text, 'html.parser')
		Announcement.my_announcement_list_fuc(soup,my_corse_name[i])
		Homework.my_homework_list_fuc(soup,my_corse_name[i])
		resorce_page = s.post("http://e-learn.cnu.ac.kr/lms/class/boardItem/doListView.dunet", data=MY_RESOURCE_FORM)
		soup = bs(resorce_page.text, 'html.parser')
		Resource.my_resource_list_fuc(soup,my_corse_name[i])

	my_all_resource = Resource.my_all_resource_fuc()
	my_all_homework = Homework.my_all_homework_fuc()
	my_all_announcement = Announcement.my_all_announcement_fuc()


def start_bot(s):
	my_course_fuc(s) #내 과목분반,과목id,과목이름 파싱
	my_all_list(s) # 내 공지,자료,과제 리스트 파싱
	
def main(input_id,userID,s):
	global my_all_announcement, my_all_homework, my_all_resource, my_major
	start_time = time.time()


	start_bot(s) #봇 시작
	
	myTable=MY_HOME.objects.get(pk=userID)
	
	myTable.createDate=datetime.now()
	myTable.announcement=my_all_announcement
	myTable.subject=my_all_homework
	myTable.resource=my_all_resource

	myTable.save()

	print("총 경과 시간 : %s 초 " % ((time.time() - start_time)))