from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm
from django.http import HttpResponse

def sign_up(request):
    print(request)
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', { 'form': form})   

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Voce logou, deu certo amigo parabems')
            login(request, user)
            return HttpResponse('BOAAAAAAAAA')
        else:
            return render(request, 'register.html', {'form': form})

def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        print(form.is_valid())

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username = username, password = password)
            print(user)
            if user:
                login(request, user)
                messages.success(request, f'Logado com sucesso')
                return redirect('index')

        messages.error(request, f'usuario ou senhas invalidos')
        return render(request,'login.html',{'form': form})



