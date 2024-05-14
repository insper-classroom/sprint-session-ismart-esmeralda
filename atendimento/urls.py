from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('aluno', views.aluno, name='aluno'),
    path('', views.index, name='index'),
    path('duvidas/', views.duvidas, name='duvidas')
    
]