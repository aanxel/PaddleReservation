from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages

from .forms import LoginForm, RegisterForm

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('reservation')
        else:
            messages.success(request, 'Ha habido un error en el inicio de sesión, pruebe de nuevo')
            form = LoginForm(request.POST)
            # redirect('login')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': LoginForm()})

def logout_user(request):
    logout(request)
    messages.success(request, 'Ha cerrado sesión correctamente')
    return redirect('reservation')

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha registrado correctamente')
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})