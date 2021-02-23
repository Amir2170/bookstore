from django.urls import path

from . import views


app_name='shop'
urlpatterns=[
	path('', views.home, name='home'),
	path('<int:product_id>/', views.detail, name='detail'),
	path('<slug:slug>/', views.category, name='category'),
]