# polls/views.py - view들을 구현
# view: 하나의 사용자 요청을 처리하는 함수
# 1. view 함수
# 2. urls.py 에 설정(url-mapping)
# 3. template(응답화면이 있는경우)

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse, resolve
from datetime import datetime 
from .models import Question, Choice


def welcome_poll_old(request):
    # view 함수 -> 1개 이상의 파라미터를 선언. (1개 필수-HttpRequest객체를 받는다.)
    now = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S초") #실행시점의 일시
    res_html = f"""<!doctype html>
<html>
    <head>
        <title>Welcome Poll</title>
    </head>
    <body>
        <h1>설문조사 APP</h1>
        현재시간: {now}
    </body>
</html>
"""
    return HttpResponse(res_html)

def welcome_poll(request):
    now = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    # template 을 이용해서 응답 페이지를 생성.
    response = render(
        request,              # HttpRequest
        "polls/welcome.html", # template파일의 경로(app_directory/templates 이후 경로)
        {"now": now, "name":"홍길동"} 
        # view가 template에 전달할 값들을 dictionary에 name-value 로 묶어서 전달.
        #    -> context value라고 한다.
    )
    # response: HttpResponse(polls/welcome.html 처리 내용)
    print("=============", type(response))
    return response
# http://127.0.0.1:8000/polls/welcome

##################################
# 설문 질문 목록을 출력하는 view
# url : polls/list
# view함수 : list
# template : polls/templates/polls/list.html

def list(request):
    # DB에서 question들을 조회
    q_list = Question.objects.all().order_by("-pub_date")
    # render(): template을 실행해서 그 결과로 HttpResponse를 반환하는 함수
    return render(request, "polls/list.html", {"question_list":q_list})


##########################33
# 개별 설문 (/polls/vote_form/질문_id)
#  - 질문 아이디 받아서 그 질문에 대해 보기를 선택할 수 있는 페이지
# polls/vote_form.html
def vote_form(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(request, "polls/vote_form.html", {"question":question})

##############################
# 투표 처리
# - choice_id 받아서 vote값을 1 증가
# - 응답 : 정상처리 투표 결과를 응답. 질문 - 보기(choice_text, votes)
#         요청 파라미터 검증 실패(아무것도 선택안하고 요청) - vote_form.html을 응답
#         DB오류, 기타 오류 - 메세지 응답(단순 텍스트)
# url: polls/vote
# view함수 : vote
# 응답 : 정상 - vote_result.html
#        오류 - vote_form.html

# view 함수에서 요청파라미터 값들을 요회
## GET: request.GET - 요청 파라미터가 dictionary로 제공된다.
## POST: request.POST - 요청 파라미터가 dictionary로 제공된다.

def vote(request):
    # 1. 요청 파라미터 조회
    # question_id request.POST['question_id'] #없으면 Exception
    question_id = request.POST.get("question_id") #없으면 None
    choice_id = request.POST.get("choice") #없으면 None
    print("question_id:", question_id, "choice_id:", choice_id)
    # 2. 요청파라미터 검증 -> choice가 선택되었는지 여부
    if choice_id:
        #votes를 1증가
        choice= Choice.objects.get(pk=choice_id)
        choice.votes += 1
        choice.save()
        # 응답 페이지로 이동
        # question = Question.objects.get(pk=question_id)
        # return render(request, "polls/vote_result.html", {"choice":choice, "question":question})
        
        # vote_result를 요청하도록 응답 - http 응답: 302, 이동할 url ==> redirect()
        # response = redirect(f"/polls/vote_result/{question_id}")
        response = redirect(reverse("polls:vote_result", args=[question_id])) #app_name이 polls인 urls.py에서 name="vote_result"인 url을 반환
        return response

    else: #선택이 안된경우(예외상황)
        question = Question.objects.get(pk=question_id) #없으면 Exception 발생. 없는 질문이면?
        return render(request, "polls/vote_form.html", {"question":question, "error_message":"선택이 안되었습니다."})
    

#####################################3
# question_id를 받아서 그 질문의 투표 결과를 응답하는 view
# url: polls/vote_result/질문_id
# view함수: vote_result
# template: polls/vote_result.html

def vote_result(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(request, "polls/vote_result.html", {"question":question})

def vote_create(request):
    http_method = request.method
    if http_method == "GET":
        return render(request, "polls/vote_create.html")
    elif http_method == "POST":
        question_text = request.POST.get("question_text")
        #같은 이름으로 여러개 값이 전달된 경우 getlist("요청파라미터이름")
        choice_list = request.POST.getlist("choice_text")
        
        #DB에 저장
        q = Question(question_text=question_text)
        q.save()
        for choice_text in choice_list:
            c = Choice(choice_text=choice_text, question=q)
            c.save()
        return redirect(reverse("polls:list"))
