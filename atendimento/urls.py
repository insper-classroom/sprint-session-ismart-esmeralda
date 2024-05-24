from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('aluno', views.aluno, name='aluno'),
    path('', views.index, name='index'),
    path('duvidas/', views.duvidas, name='duvidas'),
    path('chatbot/<str:username>/<str:useruuid>', views.chatbot, name='chatbot'),
    path('tela_colaborador/', views.mostra_conversas, name='tela_colaborador'),
    path('receberzap/', views.receber_zap, name='receber_zap'),
    path('tela_colaborador/resolve/<int:conversa_id>/', views.resolve, name='resolve'),
    path('tela_colaborador/assign_conversa/<int:conversa_id>/', views.assign_conversa, name='assign_conversa'),
    path('tela_colaborador/sendmsg/<int:telefone>/<int:conversa_id>/', views.send_msg, name='send_msg'),
    path('enviar_email/', views.mandar_email, name='mandar_email'),
    path('receber_emails/', views.receive_email, name='receive_email')

]