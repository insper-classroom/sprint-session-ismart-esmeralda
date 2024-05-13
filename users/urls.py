from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='index'),
    path('login/', views.loginview, name='index'),
]