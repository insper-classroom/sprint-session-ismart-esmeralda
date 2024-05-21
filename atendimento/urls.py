from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('aluno', views.aluno, name='aluno'),
    path('', views.index, name='index'),
    path('duvidas/', views.duvidas, name='duvidas'),
    path('chatbot/<str:username>/<str:useruuid>', views.chatbot, name='chatbot'),
    path('sendzap/<str:username>/<int:useruuid>/<str:tag>/', views.sendzap, name='sendzap'),
    path('tela_colaborador/', views.mostra_conversas, name='tela_colaborador'),
    path('cria_conversas/', views.cria_conversas, name='cria_conversas'),
    path('tela_colaborador/resolve/<int:conversa_id>/', views.resolve, name='resolve'),
    

    
]