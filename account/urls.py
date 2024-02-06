from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
	path('login/', views.login_view, name="login"),
	path('register/', views.register_view, name="register"),
	path('logout/', views.logout_view, name="logout"),
	path('update/', views.update_view, name="update"),
	path('follow/', views.follow_view, name="follow"),
	path('account/<user_id>/', views.account_view, name="account"),
	path('activate/<uidb64>/<token>/', views.activate, name="activate"),
]