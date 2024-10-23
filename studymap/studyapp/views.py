from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm
from . models import Stopwatch
from datetime import datetime


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')  # Redirect to a dashboard or another page
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = UserRegistrationForm()
    return render(request, 'studyapp/templates/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'studyapp/templates/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'studyapp/templates/dashboard.html')

def study_time(request):
    return render(request, "timer.html")

def update_time(request): # Unused right now, but useful for saving study times later
    count = Stopwatch.objects.first()
    count.time_spent = count.time_start - datetime.now()
    count.save()
    get_time = count.time_spent
    hours = get_time // 3600
    minutes = (get_time%3600) // 60
    seconds = ((get_time%3600)%60)
    time_spent = {
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
        
    }
    return render(request,"timespent.html",{"time_spent":time_spent})
