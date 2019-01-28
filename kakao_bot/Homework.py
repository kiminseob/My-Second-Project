from bs4 import BeautifulSoup as bs
import re
from myHome.models import MY_HOME
import datetime,time

my_homework = []

# Parsing my homework
def my_homework_list_fuc(soup,my_corse_name):
        homework_table = soup.find('table', {'class': 'datatable mg_t15'})
        homework_table_body = homework_table.find('tbody')
        rows = homework_table_body.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            cols.insert(0, my_corse_name)
            my_homework.append([ele for ele in cols if ele]) # Get rid of empty values

# Sort my homework
def my_all_homework_fuc():
	my_all_homework=""
	for i in range(my_homework.__len__()):
		for j in range(my_homework[i].__len__()):
			if my_homework[i].__len__() == 6:
				if ongoing_homework(my_homework.__getitem__(i)[4]): # 과제제출이 진행중이면
					if j == 0:
						my_all_homework = my_all_homework + "\n※" + my_homework.__getitem__(i)[j] + "\n"
					elif j == 2:
						my_all_homework = my_all_homework + " - " + my_homework.__getitem__(i)[j] + " "
					elif j == 3:
						my_all_homework = my_all_homework + "[" + my_homework.__getitem__(i)[j] + "~"
					elif j == 4:
						my_all_homework = my_all_homework + my_homework.__getitem__(i)[j] + "]"
					elif j == 5:
						my_all_homework = my_all_homework + " _(" + my_homework.__getitem__(i)[j] + ")\n"
			else:
				if ongoing_homework(my_homework.__getitem__(i)[3]):  # 과제제출이 진행중이면
					if j == 0:
						my_all_homework = my_all_homework + "\n※" + my_homework.__getitem__(i)[j] + "\n"
					elif j == 1:
						my_all_homework = my_all_homework + " - " + my_homework.__getitem__(i)[j] + " "
					elif j == 2:
						my_all_homework = my_all_homework + "[" + my_homework.__getitem__(i)[j] + "~"
					elif j == 3:
						my_all_homework = my_all_homework + my_homework.__getitem__(i)[j] + "]"
					elif j == 4:
						my_all_homework = my_all_homework + " _(" + my_homework.__getitem__(i)[j] + ")\n"

	if my_all_homework =="":
		my_all_homework="\n※과제가 없습니다.\n"
	return my_all_homework

# current ongoing homework
def ongoing_homework(date_end):
	date_end_array = date_end.split(".")

	date_end=""
	for i in range(3):
		date_end = date_end + date_end_array[i]
	end_date = int(date_end)
	now_date = int(time.strftime("%Y%m%d"))
	if now_date <= end_date:
		return True
	else:
		return False