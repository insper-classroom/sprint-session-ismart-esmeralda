from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'atendimento/index.html')

def aluno(request):
    return render(request, 'atendimento/aluno.html')