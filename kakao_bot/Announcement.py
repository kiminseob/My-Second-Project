from bs4 import BeautifulSoup as bs
import re
from myHome.models import MY_HOME
import datetime,time
from datetime import datetime
my_announcement = []

# Parsing my announcement
def my_announcement_list_fuc(soup,my_corse_name):

    announcement_table = soup.find_all('table', {'class': 'datatable fs_s bo_lrn'})[1]
    announcement_table_body = announcement_table.find('tbody')
    rows = announcement_table_body.find_all('tr')
	
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        cols.insert(0, my_corse_name)
        my_announcement.append([ele for ele in cols if ele])  # Get rid of empty values
		
		  
# Sort my announcement
def my_all_announcement_fuc():
	
	my_all_announcement=""
	for i in range(my_announcement.__len__()):
		if my_announcement.__getitem__(i).__len__()==3:
			if latest_date(my_announcement.__getitem__(i)[2],7):
				for j in range(3):
                    # announcement subject name duplicate check
					count = equals_announement(i)
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


# da
def latest_date(date,start):
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

 #공지사항 과목 중복 비교
def equals_announement(ai):
    count=0
    for i in range(ai):
        if my_announcement[i][0] == my_announcement[ai][0]:
            count=count+1
    return count