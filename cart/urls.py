from django.urls import path

from . import views


app_name = 'cart'
urlpatterns = [
    path('add/<slug:slug>/', views.add, name='add'),
]