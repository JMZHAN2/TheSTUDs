from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . models import Stopwatch
from django.template import loader


def study_time(request):
    timer_obj = Stopwatch.objects.first()
    get_time = timer_obj.time_spent
    hours = get_time // 3600
    minutes = (get_time%3600) // 60
    seconds = ((get_time%3600)%60)

    timespent = {
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        }
    return render(request, "timer.html",{"timespent":timespent})

def get_count(request):
    count = Stopwatch.objects.first()
    count.time_spent += 1
    count.save()
    return JsonResponse({"study_time":count.time_spent})

