from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required   
def index(request):
    return render(request, 'atendimento/index.html')

def duvidas(request):
    return render(request, 'atendimento/sobre_duvida.html')

def aluno(request):
    return render(request, 'atendimento/aluno.html')