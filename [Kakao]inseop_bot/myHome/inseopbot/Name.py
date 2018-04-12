from bs4 import BeautifulSoup as bs
import re
my_name=""
def my_name_fuc(s): # 내 이름 파싱
    global my_name
    my_page = s.get('페이지 주소')
    soup = bs(my_page.text, 'html.parser')
    my_name_span = soup.find("span", {"class": "login_after"})
    my_name = my_name_span.find("strong").text.split("님")[0]
    my_name = my_name.strip()