from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'atendimento/index.html')

@login_required
def duvidas(request):
    return render(request, 'atendimento/sobre_duvida.html')

@login_required
def aluno(request):
    return render(request, 'atendimento/aluno.html')