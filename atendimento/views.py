from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'atendimento/index.html')

def duvidas(request):
    return render(request, 'atendimento/sobre_duvida.html')

def chat_nao_atribuido(request):
    return render(request, 'atendimento/chat_nao_atribuido.html')
