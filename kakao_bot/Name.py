from bs4 import BeautifulSoup as bs
import re
my_name=""

# Parsing my name
def my_name_fuc(s):
    global my_name
    my_page = s.get('http://e-learn.cnu.ac.kr/lms/myLecture/doListView.dunet?mnid=201008840728')  # 강의목록확인
    soup = bs(my_page.text, 'html.parser')
    my_name_span = soup.find("span", {"class": "login_after"})
    my_name = my_name_span.find("strong").text.split("님")[0]
    my_name = my_name.strip()