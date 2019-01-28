from bs4 import BeautifulSoup as bs
import re
from myHome.models import MY_HOME
import sys
sys.path.insert(0,'/usr/local/lib/python3.5/dist-packages')
import requests
import datetime,time
from datetime import datetime

my_resource = []

# Get a list of all resources.
def my_resource_list_fuc(soup,my_corse_name):

    resorce_page_table = soup.find('table', {'class': 'list'})
    resorce_page_tbody = resorce_page_table.find('tbody')
    rows = resorce_page_tbody.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        cols.insert(0, my_corse_name)
        my_resource.append([ele for ele in cols if ele])  # Get rid of empty values

# Sort the list.
def my_all_resource_fuc():
	p= re.compile("\s{56}")
	my_all_resource=""
	for i in range(my_resource.__len__()):
		if my_resource.__getitem__(i).__len__()==7:
			for j in range(7):
				if latest_date(my_resource.__getitem__(i)[5],7):
					count = equals_resource(i)
                    # 과목 이름 첫번째일 경우
					if count == 0 and j==0 :
						my_all_resource = my_all_resource +"\n※" + my_resource.__getitem__(i)[j]+"\n"
					elif j==2:
						if p.search(my_resource.__getitem__(i)[j]) is not None:
							my_resource.__getitem__(i)[j]=re.split('\s{56}',my_resource.__getitem__(i)[j])[0]
						my_all_resource = my_all_resource +" - "+ my_resource.__getitem__(i)[j]
					elif j==5:
						if latest_date(my_resource.__getitem__(i)[j],0):
							my_all_resource = my_all_resource + " [" + my_resource.__getitem__(i)[j] + "]★TODAY★\n"
						elif latest_date(my_resource.__getitem__(i)[j],2):
							my_all_resource = my_all_resource + " [" + my_resource.__getitem__(i)[j] + "]★UP★\n"
						else:
							my_all_resource = my_all_resource + " [" + my_resource.__getitem__(i)[j] + "]\n"
    
	if my_all_resource =="":
		my_all_resource="\n※자료가 없습니다.\n"
	return my_all_resource


# start만큼의 기간에 대한 공지, 자료실에 내용을 가져온다.
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

#자료실 과목 중복 비교
def equals_resource(ai):
    count=0
    for i in range(ai):
        if my_resource[i][0] == my_resource[ai][0]:
            count=count+1
    return count