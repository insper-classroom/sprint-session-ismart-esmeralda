from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm
from django.http import HttpResponse

def sign_up(request):
    #
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', { 'form': form})   

    #se for um post ele vai validar o formulario e registrar o usuario no BD 
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        #se o formulario for valido ele salva o usuario no, loga, e volta pro index
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Usuário registrado com sucesso!')
            login(request, user)
            return redirect('index')
        #se o formulario for invalido ele volta pro formulario
        else:
            return render(request, 'register.html', {'form': form})

def sign_in(request):
    #se for um get renderiza o formulario
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    #se for um post ele vai validar o formulario
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username = username, password = password)
            #se o login der certo, faz isso
            if user:
                login(request, user)
                messages.success(request, f'Logado com sucesso')
                return redirect('index')
        #se o login der errado, faz isso
        messages.error(request, f'usuario ou senhas invalidos')
        return render(request,'login.html',{'form': form})



