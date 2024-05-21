from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Conversa, Mensagem
from django.contrib.contenttypes.models import ContentType
from chatbot.classificador import classifier
from users.models import CustomUser
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt




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


#Mostra as conversas daquele colaborador, filtrando por nao atribuidas e atribuidas
@staff_member_required
def mostra_conversas(request):
    colab = request.user.id
    conversas = Conversa.objects.all()
    notassigned = conversas.filter(assigned_to=None, resolved=False)
    yours = conversas.filter(assigned_to=colab, resolved=False)
    return render(request, 'atendimento/tela_colaborador.html', {'notassigned': notassigned, 'yours': yours})

#view pro colaborador atribuir uma nao atribuida a ele
@staff_member_required
def assign_conversa(request, conversa_id):
    conversa = Conversa.objects.get(id = conversa_id)
    conversa.assigned_to = request.user
    conversa.save()
    return redirect('tela_colaborador')

#view pro colaborador marcar uma conversa como resolvida
@staff_member_required
def resolve(request, conversa_id):
    conversa = Conversa.objects.get(pk=conversa_id)
    conversa.resolved = True
    conversa.save()
    return redirect('tela_colaborador')

#view pra receber a mensagem do zap e salvar no banco
@csrf_exempt
def receber_zap(request):
    if request.method == 'POST':
        data = request.POST
        user = CustomUser.objects.first()
        c1 = Conversa.objects.create(usuarios=user, tag='online')
        Mensagem.objects.create(conversa=c1, sender=user, content=data['Body'])
        return redirect('tela_colaborador')
    else:
        return redirect('tela_colaborador')
    
#views pra mandar pra url do chatbot c as informacoes do usuario na url
def chatbot(request, username, useruuid):
    
    return redirect(f'http://localhost:8502/?username={username}&useruuid={useruuid}')


def sendzap(request, username, userid, tag):
    print(f'olá. {username} tem dúvida sobre {tag}')
    return redirect('index')
    