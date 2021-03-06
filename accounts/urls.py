from django.urls import path, include

from . import views


app_name='accounts'
urlpatterns = [
	path('signup/', views.signup_view, name='signup'),
	path('logout/', views.logout_view, name='logout'),
	path('login/', views.login_view, name='login'),
]