from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('duvidas/', views.duvidas, name='duvidas'),
    path('chat_nao_atribuido/', views.chat_nao_atribuido, name='chat_nao_atribuido')
    
]