from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('duvidas/', views.duvidas, name='duvidas'),
    path('aluno/', views.aluno, name='aluno'),
    path('conversations/<str:status>/', views.mostra_conversas, name='conversations'),
    path('conversation/<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('assign_conversa/<int:conversa_id>/', views.assign_conversa, name='assign_conversa'),
    path('send_msg/<str:telefone>/<int:conversa_id>/', views.send_msg, name='send_msg'),
    path('resolve/<int:conversa_id>/', views.resolve, name='resolve'),
    path('receber_zap/', views.receber_zap, name='receber_zap'),
    path('chatbot/<str:username>/<str:useruuid>/', views.chatbot, name='chatbot'),
    path('mandar_email/', views.mandar_email, name='mandar_email'),
    path('receive_email/', views.receive_email, name='receive_email'),
]