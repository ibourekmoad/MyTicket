from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'your login was successful')
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid username or password')
            return redirect('login')
    else:
        return render(request, 'users/login.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print(request.POST)
            user = form.save(commit=False)
            user.is_customer = True
            user.save()
            messages.success(request, 'Your registration was successful log in to the app')
            return redirect('login')
        else:
            messages.error(request, 'check for errors please try again')
            return redirect('register')
    else:
        form = RegistrationForm()
        return render(request, 'users/register.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'logged out successfully')
    return redirect('login')

# still need to incorporate the forget password

