from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
from django.http import HttpResponse
from .models import Colaborador, Conversa, Usuario, Mensagem
from django.contrib.contenttypes.models import ContentType



# Create your views here.
def index(request):
    return render(request, 'atendimento/index.html')

@login_required
def duvidas(request):
    return render(request, 'atendimento/sobre_duvida.html')

@login_required
def aluno(request):
    return render(request, 'atendimento/aluno.html')


def testchat(request):
    account_sid = 'AC4001f4f9199704babdc1297dfffeabda'
    auth_token = '7f9724a8f537cec4e85ac1d86c50b660'
    client = Client(account_sid, auth_token)
    messages = client.messages.list()
    messages.reverse()
    return render(request, 'atendimento/testchat.html', {'messages': messages})

def testeregistro(request):
    user = Usuario.objects.create(nome='Alice')
    collaborator = Colaborador.objects.create(nome='Bob')
    return HttpResponse('Usuário e colaborador criados com sucesso!')

def colaborador_conversas(request, colaborador_id):
    user = Usuario.objects.get(pk=1)
    collaborator = Colaborador.objects.get(pk=colaborador_id)
    conversa = Conversa.objects.create(usuarios=user, colaboradores=collaborator)
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


