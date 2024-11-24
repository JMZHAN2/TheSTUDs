from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import Stopwatch
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from collections import defaultdict
import json


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

    # Calculate the current streak and longest streak
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


@login_required
def dashboard(request):
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

    # Do not create a stopwatch automatically
    stopwatch = user_stopwatches.first() if user_stopwatches.exists() else None

    return render(request, "timer.html", {"stopwatch": stopwatch, "all_stopwatches": user_stopwatches})


@login_required
def start_study_session(request):
    if request.method == 'POST':
        title = request.POST.get('title', 'Study Session')
        stopwatch = Stopwatch(user=request.user, title=title)
        stopwatch.save()
        return redirect('dashboard')
    return redirect('study_time')


@login_required
def study_statistics(request):
    timeframe = request.GET.get('timeframe', 'all')
    start_date = timezone.now() - timedelta(days=30)

    if timeframe == 'month':
        study_sessions = Stopwatch.objects.filter(
            user=request.user,
            time_start__gte=start_date
        ).order_by('-time_start')
    else:
        study_sessions = Stopwatch.objects.filter(user=request.user).order_by('-time_start')

    total_time = sum(session.time_spent for session in study_sessions)
    average_time = total_time / study_sessions.count() if study_sessions.exists() else 0

    all_sessions = Stopwatch.objects.filter(user=request.user)
    all_time_heatmap_data = [
        [float(session.latitude), float(session.longitude), session.time_spent]
        for session in all_sessions if session.latitude and session.longitude
    ]

    monthly_sessions = Stopwatch.objects.filter(user=request.user, time_start__gte=start_date)
    monthly_heatmap_data = [
        [float(session.latitude), float(session.longitude), session.time_spent]
        for session in monthly_sessions if session.latitude and session.longitude
    ]

    context = {
        'study_sessions': study_sessions,
        'total_time': int(total_time),
        'average_time': int(average_time),
        'all_time_heatmap_data': json.dumps(all_time_heatmap_data),
        'monthly_heatmap_data': json.dumps(monthly_heatmap_data),
        'timeframe': timeframe,
    }
    return render(request, 'study_statistics.html', context)


@login_required
def finish_session(request):
    if request.method == "POST":
        try:
            time_spent = int(request.POST.get("time_spent", 0))
            latitude_ = float(request.POST.get("latitude", 0)) if request.POST.get("latitude") else None
            longitude_ = float(request.POST.get("longitude", 0)) if request.POST.get("longitude") else None
            session_title = request.POST.get("session_title", "Study Session").strip()

            if time_spent <= 0:
                error_message = "Cannot save a session 0 seconds long."
                return render(request, "timer.html", {
                    "error_message": error_message,
                    "latitude": latitude_,
                    "longitude": longitude_,
                    "session_title": session_title,
                })

            stopwatch = Stopwatch.objects.create(
                user=request.user,
                time_spent=time_spent,
                title=session_title,
                latitude=latitude_,
                longitude=longitude_,
            )

            hours = stopwatch.time_spent // 3600
            minutes = (stopwatch.time_spent % 3600) // 60
            seconds = stopwatch.time_spent % 60

            return render(request, "finish-session.html", {
                "time_spent": stopwatch.get_duration(),
                "hours": hours,
                "minutes": minutes,
                "seconds": seconds,
            })
        except ValueError:
            messages.error(request, "Invalid session data.")
            return redirect('study_time')

    return render(request, "finish-session.html")