from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
	path('subscription/', views.subscription_view, name="subscription"),
	path('<year>/<month>/<day>/<slug:slug>/', views.detail_view, name="detail"),
	path('search/', views.search_view, name="search"),
	path('', views.home_view, name="home"),
	path('like', views.like_view, name="like"),
	path('subscribe', views.subscribe_view, name="subscribe"),
	path('<tag>/', views.home_view, name="home"),
	path('<author>/', views.home_view, name="home"),
]