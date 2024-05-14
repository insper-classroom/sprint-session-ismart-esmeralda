from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signupview, name='registro'),
    path('login/', views.loginview, name='login'),
]