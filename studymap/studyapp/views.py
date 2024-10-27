from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm
from . models import Stopwatch
from datetime import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required




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

    study_sessions = Stopwatch.objects.filter(user=request.user).order_by('-time_start')[:5]
    streak = Stopwatch.calculate_study_streak(request.user)

    context = {
        'study_sessions': study_sessions,
        'streak': streak,
    }
    return render(request, 'dashboard.html', context)

@login_required
def study_time(request):
    stopwatch, created = Stopwatch.objects.get_or_create(user=request.user, defaults={"title": "Study Session"})
    
    return render(request, "timer.html", {"stopwatch": stopwatch})
    

@login_required
def start_study_session(request):
    
    if request.method == 'POST':
        title = request.POST.get('title') 
        stopwatch = Stopwatch(user=request.user, title=title)
        stopwatch.save()
        return redirect('dashboard')

@login_required
def finish_session(request):
    if request.method == "POST":
        stopwatch_id = request.POST.get("stopwatch_id")
        #print(f"Stopwatch ID received: {stopwatch_id}")
        time_spent = request.POST.get("time_spent")
        stopwatch = get_object_or_404(Stopwatch, id=stopwatch_id, user=request.user)

        # Calculate the time spent
        current_time = timezone.now()
        #time_diff = (current_time - stopwatch.time_start).total_seconds()
        
        
        # Update time_spent
        stopwatch.time_spent = int(time_spent)
        stopwatch.save()

        # Calculate hours, minutes, and seconds for the success message
        hours = stopwatch.time_spent // 3600
        minutes = (stopwatch.time_spent % 3600) // 60
        seconds = stopwatch.time_spent % 60

        # Create a success message
        messages.success(request, f"Good work! You studied for {hours} hours, "
                                  f"{minutes} minutes, and "
                                  f"{seconds} seconds.")

        # Optionally render a response or redirect
        return render(request, "finish-session.html", {"time_spent": stopwatch.get_duration()})
    
    # Handle cases where the method is not POST
    return render(request, "finish-session.html")





"""def update_time(request): # Unused right now, but useful for saving study times later
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
    return render(request,"timespent.html",{"time_spent":time_spent})"""
