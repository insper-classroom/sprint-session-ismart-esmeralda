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

    #mudar pro nome certo dps, ja q ta no NA, pode atribuir ou resolver a conversa
    path('side_nao_atribuido/resolve/<int:conversa_id>/', views.resolve, name='resolve'),
    path('side_nao_atribuido/assign_conversa/<int:conversa_id>/', views.assign_conversa, name='assign_conversa'),

    #resolve na pagina do minhas conversas
    path('side_minhas_conversas/resolve/<int:conversa_id>/', views.resolve, name='resolve'),

    path('side_nao_atribuido/sendmsg/<int:telefone>/<int:conversa_id>/', views.send_msg, name='send_msg_nao_atribuido'),

    path('side_minhas_conversas/sendmsg/<int:telefone>/<int:conversa_id>/', views.send_msg, name='send_msg_minhas_conversas'),

    path('duvidas/', views.duvidas, name='duvidas'),
    path('colaborador/', views.colaborador, name='colaborador'),
    path('side_nao_atribuido/', views.side_nao_atribuido, name='side_nao_atribuido'),
    path('side_minhas_conversas/', views.side_minhas_conversas, name='side_minhas_conversas'),
    path('chat/', views.chat, name='chat'),

    #abrir os chats
    path('side_nao_atribuido/chat_nao_atribuido/<int:conversa_id>/', views.chat_nao_atribuido,
    name='chat_nao_atribuido'),
    path('side_minhas_conversas/chat_minhas_conversas/<int:conversa_id>/', views.chat_minhas_conversas, name='chat_minhas_conversas'),

    path('mandar_email/', views.mandar_email, name='mandar_email'),
    path('receive_email/', views.receive_email, name='receive_email'),
    
]