from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
	path('', views.home_view, name="home"),
	path('<tag>/', views.home_view, name="home"),
	path('<year>/<month>/<day>/<slug:slug>/', views.detail_view, name="detail"),
	path('search/', views.search_view, name="search"),
]