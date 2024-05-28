from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('aluno', views.aluno, name='aluno'),
    path('', views.index, name='index'),
    path('duvidas/', views.duvidas, name='duvidas'),
    path('chatbot/<str:username>/<str:useruuid>', views.chatbot, name='chatbot'),
    path('tela_colaborador/', views.mostra_conversas, name='tela_colaborador'),

    #views que fica recebendo POST quando um zap novo chega
    path('receberzap/', views.receber_zap, name='receber_zap'),

    #redireciona de volta pro side nao atribuido qnd resolve uma duvida ou pega uma
    path('side_nao_atribuido/resolve/<int:conversa_id>/', views.resolveNA, name='resolve'),
    path('side_nao_atribuido/assign_conversa/<int:conversa_id>/', views.assign_conversa, name='assign_conversa'),

    #redireciona de volta pro side minhas conversas qnd resolve uma duvida do minhas conversas
    path('side_minhas_conversas/resolve/<int:conversa_id>/', views.resolveYOURS, name='resolve'),

    path('checar_tempo/', views.check_and_resolve_conversations, name='checar_tempo'),

    #mandar zap de conversa em nao atribuido
    path('side_nao_atribuido/sendmsg/<int:telefone>/<int:conversa_id>/', views.send_msg, name='send_msg_nao_atribuido'),

    #mandar zap em conversa em minhas conversas
    path('side_minhas_conversas/sendmsg/<int:telefone>/<int:conversa_id>/', views.send_msg, name='send_msg_minhas_conversas'),


    #redireciona para as categorias de chat de acordo c a classificacao
    path('side_nao_atribuido/', views.side_nao_atribuido, name='side_nao_atribuido'),
    path('side_minhas_conversas/', views.side_minhas_conversas, name='side_minhas_conversas'),

    #abrir os chats
    path('side_nao_atribuido/chat_nao_atribuido/<int:conversa_id>/', views.chat_nao_atribuido,
    name='chat_nao_atribuido'),
    path('side_minhas_conversas/chat_minhas_conversas/<int:conversa_id>/', views.chat_minhas_conversas, name='chat_minhas_conversas'),

    path('side_minhas_conversas/mandar_email/<str:user_email>/<int:conversa_id>/', views.mandar_email, name='mandar_email'),
    
    #view pra ficar periodicamente checando novos emails
    path('receive_email/', views.receive_email, name='receive_email'),

    path('colaborador/', views.colaborador, name='colaborador'),
    

    #estatisticas
    path('estatisticas/', views.estatisticas, name='estatisticas'),
]