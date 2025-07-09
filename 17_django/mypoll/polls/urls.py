# polls/urls.py - polls app의 url-mapping을 설정
## url - view

from django.urls import path
from . import views

urlpatterns = [
    path("welcome", views.welcome_poll, name="welcome"),
    path("list", views.list, name="list"),
    path("vote_form/<int:question_id>", views.vote_form, name="vote_form"),
    path("vote", views.vote, name="vote"),
    path("vote_result/<int:question_id>", views.vote_result, name="vote_result"),
    path("vote_create", views.vote_create, name="vote_create"),
    path("", views.list, name="polls_main")
]
app_name = "polls"