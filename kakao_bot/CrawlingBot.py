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

my_course_id = []
my_class_no = []
my_corse_name = []
my_corse_num =0

my_all_resource=""
my_all_homework=""
my_all_announcement=""

MY_CLASS_FORM={
	#class form
}
MY_RESOURCE_FORM={
	#resource form
}

# Get my course name, id, number
def my_course_fuc(s): ##강의실 ID 파싱
	global my_corse_num,my_corse_name,my_course_id,my_class_no
	my_page = s.get('http://e-learn.cnu.ac.kr/lms/myLecture/doListView.dunet?mnid=201008840728')  # 강의목록확인
	soup = bs(my_page.text, 'html.parser')
	temp = soup.findAll("a", {"class": "classin2"})
	count = temp.__len__()
	my_corse_num = count
	temp2 = temp.__str__()

	p = re.compile('course.id..\w{23}.')
	p2 = re.compile('class_no..\d\d')
	m = p.findall(temp2)
	m2 = p2.findall(temp2)

	name_splited_temp = temp2.split("<br/>")

	for i in range(count):
		my_course_id.append(m[i].split('"')[1])
		my_class_no.append(m2[i].split('"')[1])
		my_corse_name.append(name_splited_temp[i].split('"">')[1].strip())

#Get my announcement, homework, resource file list
def my_all_list(s):
	global my_all_announcement,my_all_homework,my_all_resource

	# All classroom
	for i in range(my_corse_num):
		MY_CLASS_FORM['class_no'] = my_class_no[i]
		MY_CLASS_FORM['course_id'] = my_course_id[i]
		homework_page = s.post('http://e-learn.cnu.ac.kr/lms/class/classroom/doViewClassRoom_new.dunet', data=MY_CLASS_FORM)

		# Bring information about one classroom.
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
	# My subjects, subject id, subject name parsing
	my_course_fuc(s)
	# Parsing my announcement, homework, resource file list
	my_all_list(s)

def main(input_id,userID,s):
	global my_all_announcement, my_all_homework, my_all_resource, my_major
	start_time = time.time()

	# Bot start
	start_bot(s)
	
	myTable=MY_HOME.objects.get(pk=userID)
	
	myTable.createDate=datetime.now()
	myTable.announcement=my_all_announcement
	myTable.subject=my_all_homework
	myTable.resource=my_all_resource

	myTable.save()

	print("총 경과 시간 : %s 초 " % ((time.time() - start_time)))