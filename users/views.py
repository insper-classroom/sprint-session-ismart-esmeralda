from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.http import HttpResponseRedirect


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def loginview(request):
    if request.method == 'GET':
        return render(request, 'users/login.html')

    elif request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username = email, password = password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return HttpResponseRedirect('/admin')
            else:
                return HttpResponseRedirect('/')
        else:
            return HttpResponse('deu ruim pae')