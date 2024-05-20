from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
from django.http import HttpResponse, JsonResponse
from .models import Colaborador, Conversa, Usuario, Mensagem
from django.contrib.contenttypes.models import ContentType
from chatbot.classificador import classifier
import redis
from rest_framework.response import Response
from rest_framework.decorators import api_view




# Create your views here.
def index(request):
    return render(request, 'atendimento/index.html')

@login_required
def duvidas(request):
    return render(request, 'atendimento/sobre_duvida.html')

@login_required
def aluno(request):
    print(request.user.uuid)
    return render(request, 'atendimento/aluno.html')


#APENAS PARA FINS DE TESTE
def testchat(request):
    account_sid = 'AC4001f4f9199704babdc1297dfffeabda'
    auth_token = '7f9724a8f537cec4e85ac1d86c50b660'
    client = Client(account_sid, auth_token)
    messages = client.messages.list()
    messages.reverse()
    return render(request, 'atendimento/testchat.html', {'messages': messages})


#APENAS PARA FINS DE TESTE
def testeregistro(request):
    user = Usuario.objects.create(nome='Alice')
    collaborator = Colaborador.objects.create(nome='Bob')
    return HttpResponse('Usuário e colaborador criados com sucesso!')


#APENAS PARA FINS DE TESTE
def colaborador_conversas(request, colaborador_id):
    user = Usuario.objects.get(pk=1)
    collaborator = Colaborador.objects.get(pk=colaborador_id)
    conversa = Conversa.objects.create(usuarios=user, colaboradores=collaborator)
    # conversa.set_tag(classifier(('online')))
    # print(conversa.get_tag())
    Mensagem.objects.create(conversa=conversa, sender=user, content='Hello, Bob!')
    Mensagem.objects.create(conversa=conversa, sender=collaborator, content='Hi, Alice!')
    conversa2 = Conversa.objects.create(usuarios = user, colaboradores = collaborator)
    Mensagem.objects.create(conversa = conversa2, sender = user, content = 'hell imakmfr')
    Mensagem.objects.create(conversa = conversa2, sender = collaborator, content = 'hi imakmfr') 

    for mensagem in conversa.mensagens.all():
        print(mensagem.content)

    
    colaborador = Colaborador.objects.get(pk = colaborador_id)
    conversas = Conversa.objects.filter(colaboradores = colaborador)
    return render(request, 'atendimento/testconversas.html', {'colaborador': colaborador, 'conversas': conversas})

#views pra mandar pra url do chatbot c as informacoes do usuario na url
def chatbot(request, username, useruuid):
    #pega o token desse usuario 
    #passa o token como parametro da url
    
    return redirect(f'http://localhost:8501/?username={username}&useruuid={useruuid}')

# @api_view(['POST', 'GET'])
# def api_senduser(request):

#         username = request.user.username
#         userid = request.user.id
#         return JsonResponse({"username": username, "userid": userid})

def sendzap(request, username, userid, tag):
    print(f'olá. {username} tem dúvida sobre {tag}')
    return redirect('index')
    