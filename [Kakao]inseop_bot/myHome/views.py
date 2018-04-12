from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from myHome.inseopbot import Login
from myHome.inseopbot import Name
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
		
	p = re.compile('\d{9}')
	m = p.match(content_name)
	
	if content_name =="시작하기":
		if registered_user:
			nowDateSplit = str(row.createDate).split(":")
			nowDate = nowDateSplit[0]+"시"+nowDateSplit[1]
			all_txt = "보시는 내용은 "+nowDate+"분에 생성된 정보입니다. 갱신을 원하시면 [내용 갱신하기]버튼을 눌러주세요.\n\n"+"♠최근 1주일 공지 사항♠\n"+row.announcement+"\n♠진행중인 과제♠\n"+row.subject+"\n♠최근 1주일 자료실♠\n"+row.resource+"\n\n["+nowDate+"분에 갱신됨]"  
			return JsonResponse(
				{
					'message':{
						'text': all_txt
					},
					'keyboard':{
						'type': 'buttons',
						'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기']
					}
					
				}
			)
		else:
			return JsonResponse(
				{
					'message':{
						'text': '안녕하세요 :)\n학번을 입력해주세요.'
					}
				}
			)
	if content_name=="처음부터 다시 시작하기":
		return JsonResponse(
			{
				'message':{
					'text': '안녕하세요 :)\n학번을 입력해주세요.'
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
					'text': "업데이트 중입니다. 10초 정도 소요됩니다 :)\n잠시 기다리신 후 보기 버튼을 눌러 갱신 시간을 확인해주세요!"
				},
				'keyboard':{
					'type': 'buttons',
					'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기']
				}
			}
		
		)
	if content_name =="전체 모아보기" or content_name =="공지보기"or content_name =="과제보기"or content_name =="자료실보기":
		if row.subject=="" and row.announcement=="" and row.resource=="":
			return JsonResponse(
				{
					'message':{
						'text': "조금만 더 기다려주세요.."
					},
					'keyboard':{
						'type': 'buttons',
						'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기']
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
						'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기']
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
							'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기']
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
							'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기']
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
							'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기']
						}
						
					}
				)	
	if m != None: #학번 입력
		if Login.login(content_name,True,userID):
			myTable=MY_HOME(name=Name.my_name, userID=userID,studentNum=content_name,major="",createDate=datetime.now(),announcement="",subject="",resource="")
			myTable.save()
			return JsonResponse(
				{
					'message':{
						'text': "존재하는 학번입니다!\n이름을 입력해주세요\n(학번과 이름이 일치해야해요)\n학번을 다시 입력하시려면 학번을 입력해주세요 :)"
					}
				}
			)
		else:
			return JsonResponse(
				{
					'message':{
						'text': "존재하지 않는 학번이네요 :(\n다시 입력해주세요!"
					}
				}
			)
	
	
	if content_name==row.name:
		Login.login(row.studentNum,False,userID)
		return JsonResponse(
			{
				'message':{
					'text': "로그인하여 정보를 읽어들이고 있어요 :) 5~10초 정도 기다리신 후 모아보기 버튼을 눌주세요"
				},
				'keyboard':{
					'type': 'buttons',
					'buttons':['전체 모아보기','공지보기','과제보기','자료실보기','내용 갱신하기','처음부터 다시 시작하기']
				}
			}
		
		)
	
	else:
		return JsonResponse(
			{
				'message':{
					'text': "잘못된 입력이네요 :(\n다시 입력해주세요!"
				}
			}
		
		)
