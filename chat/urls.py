from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat_home, name="chat_home"),
    path("start/", views.start_chat, name="start_chat"),
    path("search/", views.search_chat, name="search_chat"),
    path("room/", views.chat_room, name="chat_room"),
    path("send/", views.send_message, name="send_message"),
    path("fetch/", views.fetch_messages, name="fetch_messages"),
]