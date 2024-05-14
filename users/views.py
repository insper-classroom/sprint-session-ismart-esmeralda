from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.http import HttpResponseRedirect


def signupview(request):
    """View para registro de usuário"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            #aqui eh pra onde vai redirecionar o usuário depois de registrar
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def loginview(request):
    """View para login de usuário"""
    if request.method == 'GET':
        return render(request, 'users/login.html')

    elif request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username = email, password = password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                #se o usuario for colaborador, redireciona pra ca 
                return HttpResponseRedirect('/admin')
            else:
                #caso contrario ele é aluno, e redireciona pra ca
                return redirect('index')
        else:
            return HttpResponse('deu ruim pae')