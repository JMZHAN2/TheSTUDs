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
import json
from datetime import timedelta
from collections import defaultdict


########## Study Streak Visualization
def study_report_view(request):
    user = request.user
    # Get all study sessions for the logged-in user, ordered by start time
    sessions = Stopwatch.objects.filter(user=user).order_by('time_start')
    
    # Calculate total study time per day
    daily_study_times = defaultdict(int)
    for session in sessions:
        day = session.time_start.date()
        daily_study_times[day] += session.time_spent

    # Calculate the current streak and longest streak using the model method or directly here
    current_streak = Stopwatch.calculate_study_streak(user)
    longest_streak = 0
    unique_dates = sorted(daily_study_times.keys(), reverse=True)

    temp_streak = 0
    last_date = None
    for date in unique_dates:
        if last_date is None or (last_date - date).days == 1:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
            last_date = date
        else:
            temp_streak = 1
            last_date = date

    # Calculate average study time per day
    total_days = len(daily_study_times)
    total_study_time = sum(daily_study_times.values())
    average_study_time = total_study_time / total_days if total_days > 0 else 0

    # Pass data to the template
    context = {
        'current_streak': current_streak,
        'longest_streak': longest_streak,
        'average_study_time': average_study_time,
        'daily_study_times': dict(daily_study_times),
    }
    return render(request, 'study_report.html', context)


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
    user_stopwatches = Stopwatch.objects.filter(user=request.user).order_by('-time_start')
    
    if not user_stopwatches.exists():
        stopwatch = Stopwatch.objects.create(user=request.user, title="Study Session")
    else:
        stopwatch = user_stopwatches.first()  
    
    return render(request, "timer.html", {"stopwatch": stopwatch, "all_stopwatches": user_stopwatches})


@login_required
def start_study_session(request):
    if request.method == 'POST':
        title = request.POST.get('title') 
        stopwatch = Stopwatch(user=request.user, title=title)
        stopwatch.save()
        return redirect('dashboard')

@login_required
def study_statistics(request):
    # Get the timeframe parameter from the request (default to 'all')
    timeframe = request.GET.get('timeframe', 'all')

    # Calculate start_date for the past month
    start_date = timezone.now() - timedelta(days=30)

    # Retrieve study sessions based on the timeframe
    if timeframe == 'month':
        study_sessions = Stopwatch.objects.filter(
            user=request.user,
            time_start__gte=start_date
        ).order_by('-time_start')
    else:
        study_sessions = Stopwatch.objects.filter(user=request.user).order_by('-time_start')

    # Calculate total study time
    total_time = sum(session.time_spent for session in study_sessions)

    # Calculate average session time
    if study_sessions.exists():
        average_time = total_time / study_sessions.count()
    else:
        average_time = 0

    # Prepare heatmap data
    # All-time data
    all_sessions = Stopwatch.objects.filter(user=request.user)
    all_time_heatmap_data = []
    for session in all_sessions:
        if session.latitude and session.longitude:
            intensity = session.time_spent
            all_time_heatmap_data.append([float(session.latitude), float(session.longitude), intensity])

    # Monthly data
    monthly_sessions = Stopwatch.objects.filter(
        user=request.user,
        time_start__gte=start_date
    )
    monthly_heatmap_data = []
    for session in monthly_sessions:
        if session.latitude and session.longitude:
            intensity = session.time_spent
            monthly_heatmap_data.append([float(session.latitude), float(session.longitude), intensity])

    # Convert heatmap data to JSON
    all_time_heatmap_data_json = json.dumps(all_time_heatmap_data)
    monthly_heatmap_data_json = json.dumps(monthly_heatmap_data)

    # Pass data to the template
    context = {
        'study_sessions': study_sessions,
        'total_time': int(total_time),
        'average_time': int(average_time),
        'all_time_heatmap_data': all_time_heatmap_data_json,
        'monthly_heatmap_data': monthly_heatmap_data_json,
        'timeframe': timeframe,
    }
    return render(request, 'study_statistics.html', context)


@login_required
def finish_session(request):
    if request.method == "POST":
        stopwatch_id = request.POST.get("stopwatch_id")

        try:
            time_spent = int(request.POST.get("time_spent", 0))
        except ValueError:
            time_spent = 0

        # Convert latitude and longitude before passing
        try:
            latitude_ = float(request.POST.get("latitude"))
        except (TypeError, ValueError):
            latitude_ = None
        try:
            longitude_ = float(request.POST.get("longitude"))
        except (TypeError, ValueError):
            longitude_ = None

        session_title = request.POST.get("session_title", "Study Session").strip()

        if time_spent <= 0:
            # Redirect to the timer page with an error message
            error_message = "Cannot save a session 0 seconds long"
            return render(request, "timer.html", {
                "error_message": error_message,
                "latitude": latitude_,
                "longitude": longitude_,
                "session_title": session_title,
            })

        # Create a new Stopwatch instance for each session
        stopwatch = Stopwatch.objects.create(
            user=request.user,
            time_spent=int(time_spent),
            title= session_title,  
            latitude = float(latitude_),
            longitude = float(longitude_),

        )

        # Calculate hours, minutes, and seconds for the success message
        hours = stopwatch.time_spent // 3600
        minutes = (stopwatch.time_spent % 3600) // 60
        seconds = stopwatch.time_spent % 60

        return render(request, "finish-session.html", {
            "time_spent": stopwatch.get_duration(),
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        })
    
    # Handle cases where the method is not POST
    return render(request, "finish-session.html")



