from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from myHome.inseopbot import Login
from myHome.inseopbot import weather
from myHome.models import MY_HOME
import re
from datetime import datetime



# Create your views here.
def keyboard(request):
	
	return JsonResponse(
	{
	  'type': 'buttons',
	  'buttons' : ['시작하기']
	}
  )
@csrf_exempt 
def message(request):
	
	json_str = (request.body).decode('utf-8')
	received_json = json.loads(json_str)
	content_name = received_json['content']
	userID = received_json['user_key']
	registered_user=False
	try:
		row = MY_HOME.objects.get(pk=userID)
		registered_user=True
	except Exception as e:
		print(e)

	p = re.compile('\d{9}/\d{8}') # 학번 정규표현식
	m = p.match(content_name)



	if content_name =="시작하기":
		if registered_user:

			if row.studentNum =="201202166/19931003":
				return JsonResponse(
					{
						'message': {
							'text': "인섭 ㅎㅇ"
						},
						'keyboard': {
							'type': 'buttons',
							'buttons': ['전체 모아보기', '공지보기', '과제보기', '자료실보기', '내용 갱신하기', '처음부터 다시 시작하기',
										'충남대 현재 날씨 확인하기']
						}

					}
				)
			else:
				return JsonResponse(
					{
						'message': {
							'text': "★"+row.name+"님 환영합니다.★"
						},
						'keyboard': {
							'type': 'buttons',
							'buttons': ['전체 모아보기', '공지보기', '과제보기', '자료실보기', '내용 갱신하기', '처음부터 다시 시작하기',
										'충남대 현재 날씨 확인하기']
						}

					}
				)
		else:
			return JsonResponse(
				{
					'message':{
						'text': '안녕하세요🙌\n사이버캠퍼스의 공지,과제,자료실 업로드 사항을 한번에 모아보기 하실 수 있습니다.\n단, 비밀번호가 생년월일인 경우만 이용 가능합니다. 👉학번/생년월일을 아래와 같은 형식으로 입력해주세요.(ex.201802145/19991008)'
					}
				}
			)
	if content_name=="처음부터 다시 시작하기":
		return JsonResponse(
			{
				'message':{
					'text': '안녕하세요🙌\n사이버캠퍼스의 공지,과제,자료실 업로드 사항을 한번에 모아보기 하실 수 있습니다.\n단, 비밀번호가 생년월일인 경우만 이용 가능합니다. 👉학번/생년월일을 아래와 같은 형식으로 입력해주세요.(ex.201802145/19991008)'
				}
			}
		)
		
	if content_name=="내용 갱신하기":
		row.announcement=""
		row.subject=""
		row.resource=""
		row.save()
		Login.login(row.studentNum,False,userID)
		return JsonResponse(
			{
				'message':{
					'text': "업데이트 중입니다.\n10초 정도 기다리신 후 아래의 버튼을 눌러 이용해 주세요.\n.......🐌.......🐌.......🐌......🐌......"
				},
				'keyboard':{
					'type': 'buttons',
					'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기','충남대 현재 날씨 확인하기']
				}
			}
		
		)
	if content_name =="전체 모아보기" or content_name =="공지보기"or content_name =="과제보기"or content_name =="자료실보기":
		if row.subject=="" and row.announcement=="" and row.resource=="":
			return JsonResponse(
				{
					'message':{
						'text': "조금만 더 기다려 주세요 \n......🐌.....🐌.....🐌.....🐌......"
					},
					'keyboard':{
						'type': 'buttons',
						'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기','충남대 현재 날씨 확인하기']
					}
				}
			)
		nowDateSplit = str(row.createDate).split(":")
		nowDate = nowDateSplit[0]+"시"+nowDateSplit[1]
	if content_name =="전체 모아보기":
		all_txt = "♠최근 1주일 공지 사항♠\n"+row.announcement+"\n♠진행중인 과제♠\n"+row.subject+"\n♠최근 1주일 자료실♠\n"+row.resource+"\n["+nowDate+"분에 갱신됨]"
		return JsonResponse(
			{
				'message':{
					'text': all_txt
				},
				'keyboard':{
					'type': 'buttons',
					'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기','충남대 현재 날씨 확인하기']
				}

			}
		)
	if content_name=="공지보기":
		all_txt = "♠최근 1주일 공지 사항♠\n"+row.announcement+"\n["+nowDate+"분에 갱신됨]"
		return JsonResponse(
				{
					'message':{
						'text': all_txt
					},
					'keyboard':{
						'type': 'buttons',
						'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기','충남대 현재 날씨 확인하기']
					}

				}
			)
	if content_name=="과제보기":
		all_txt = "♠진행중인 과제♠\n"+row.subject+"\n["+nowDate+"분에 갱신됨]"
		return JsonResponse(
				{
					'message':{
						'text': all_txt
					},
					'keyboard':{
						'type': 'buttons',
						'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기','충남대 현재 날씨 확인하기']
					}

				}
			)
	if content_name=="자료실보기":
		all_txt = "♠최근 1주일 자료실♠\n"+row.resource+"\n["+nowDate+"분에 갱신됨]"
		return JsonResponse(
				{
					'message':{
						'text': all_txt
					},
					'keyboard':{
						'type': 'buttons',
						'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기','충남대 현재 날씨 확인하기']
					}

				}
			)
	if m != None: #학번,생년월일 입력
		if Login.login(content_name,True,userID):
			myTable=MY_HOME(name=Login.my_name, userID=userID,studentNum=content_name,major=Login.my_major,createDate=datetime.now(),announcement="",subject="",resource="")
			myTable.save()
			return JsonResponse(
				{
					'message':{
						'text': "로그인 되었습니다.✔\n이름을 입력해주세요.👀"
					}
				}
			)
		else:
			return JsonResponse(
				{
					'message':{
						'text': "존재하지 않는 학번이거나 비밀번호가 틀렸습니다.👀!\n다시 입력해 주세요 '<')/ ~~!"
					}
				}
			)


	if content_name==row.name:
		Login.login(row.studentNum,False,userID)
		return JsonResponse(
			{
				'message':{
					'text': "이름이 일치합니다.\n정보를 읽어들이고 있습니다.\n10초 정도 기다리신 후 아래의 버튼을 눌러 이용해 주세요\n........🐌.....🐌......🐌.....🐌........"
				},
				'keyboard':{
					'type': 'buttons',
					'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기','충남대 현재 날씨 확인하기']
				}
			}
		
		)

	if content_name=='충남대 현재 날씨 확인하기':
		weather.find_weather()
		return JsonResponse(
			{
				'message':{
					'text': "충남대(궁동)날씨 : "+weather.todayTemp+"\n("+weather.compareTemp+")"
				},
				'keyboard':{
					'type': 'buttons',
					'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기','충남대 현재 날씨 확인하기']
				}
			}
		
		)


	else:
		return JsonResponse(
			{
				'message':{
					'text': "잘못된 입력이네요.👀!\n다시 입력해 주세요!"
				}
			}

		)
