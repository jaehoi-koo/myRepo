from django.urls import path
from .views import (
    chat_message,
    ChatRoomListView,
    ChatRoomDetailView,
    MessageListView
)


urlpatterns = [
    # 새로운 RESTful API
    path('chatrooms/', ChatRoomListView.as_view(), name='chatroom-list'),
    path('chatrooms/<int:room_id>/', ChatRoomDetailView.as_view(), name='chatroom-detail'),
    path('chatrooms/<int:room_id>/messages/', MessageListView.as_view(), name='message-list'),

    # 기존 API (호환성을 위해 유지)
    path('chat_message/<str:message>/', chat_message, name='chat_message'),
]