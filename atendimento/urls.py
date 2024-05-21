from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('aluno', views.aluno, name='aluno'),
    path('', views.index, name='index'),
    path('duvidas/', views.duvidas, name='duvidas'),
    # path('testchat/', views.testchat, name='testchat'),
    # path('colaborador/<int:colaborador_id>/conversas/', views.colaborador_conversas, name='colaborador_conversas'),
    # path('testeregistro/', views.testeregistro, name='testeregistro'),
    path('chatbot/<str:username>/<str:useruuid>', views.chatbot, name='chatbot'),
    path('sendzap/<str:username>/<int:useruuid>/<str:tag>/', views.sendzap, name='sendzap'),
    path('tela_colaborador/', views.tela_colaborador, name='tela_colaborador'),
    path('cria_conversas/', views.cria_conversas, name='cria_conversas'),

    

    
]