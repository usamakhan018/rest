from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
	path('chat/<user_id>/', views.chat_view, name="chat"),
	path('get_or_create_chat_view/', views.get_or_create_chat_view, name="get_or_create_chat_view"),
]