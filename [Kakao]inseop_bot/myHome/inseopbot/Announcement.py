from bs4 import BeautifulSoup as bs
import re
from myHome.models import MY_HOME
import datetime,time
from datetime import datetime
my_announcement = []#모든 과목의 공지사항

def my_announcement_list_fuc(soup,my_corse_name): # 공지 리스트 가져오기

    announcement_table = soup.find_all('table', {'class': 'datatable fs_s bo_lrn'})[1]
    announcement_table_body = announcement_table.find('tbody')
    rows = announcement_table_body.find_all('tr')
	
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        cols.insert(0, my_corse_name)
        my_announcement.append([ele for ele in cols if ele])  # Get rid of empty values
		
		  

def my_all_announcement_fuc(): #내 공지 정렬
	
	my_all_announcement=""
	for i in range(my_announcement.__len__()):
		if my_announcement.__getitem__(i).__len__()==3:
			if latest_date(my_announcement.__getitem__(i)[2],7):
				for j in range(3):
					count = equals_announement(i)# 공지 과목이름중복 체크
					if count is 0:
						if j == 0:
							my_all_announcement = my_all_announcement + "\n※" + my_announcement.__getitem__(i)[j] + "\n"
						elif j == 1:
							my_all_announcement = my_all_announcement + " - " + my_announcement.__getitem__(i)[j]
					elif j == 1:
						my_all_announcement = my_all_announcement + " - " + my_announcement.__getitem__(i)[j]
					if j == 2:
						if latest_date(my_announcement.__getitem__(i)[j],0):
							my_all_announcement = my_all_announcement + " [" + my_announcement.__getitem__(i)[j]  + "]★TODAY★\n"
						elif latest_date(my_announcement.__getitem__(i)[j],2):
							my_all_announcement = my_all_announcement + " [" + my_announcement.__getitem__(i)[j]  + "]★UP★\n"
						else:
							my_all_announcement = my_all_announcement + " [" + my_announcement.__getitem__(i)[j] + "]\n"
	if my_all_announcement =="":
		my_all_announcement="\n※공지가 없습니다.\n"
	return my_all_announcement
def latest_date(date,start): #start만큼의 기간동안 공지, 자료실에 대한 내용을 보여준다.
    date_array = date.split(".")
    yy = int(date_array[0])
    mm = int(date_array[1])
    dd = int(date_array[2])
    date= datetime(yy,mm,dd)
    date_gap = datetime.today()-date
    if  date_gap.days <= start:
        return True
    else:
        return False

		
def equals_announement(ai): #공지사항 과목 중복 비교
    count=0
    for i in range(ai):
        if my_announcement[i][0] == my_announcement[ai][0]:
            count=count+1
    return count