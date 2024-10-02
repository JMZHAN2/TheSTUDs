from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . models import Stopwatch
from django.template import loader


def study_time(request):
    timer_obj = Stopwatch.objects.first()
    get_time = timer_obj.time_spent
    return render(request, "timer.html",{"get_time":get_time})

def get_count(request):
    count = Stopwatch.objects.first()
    count.time_spent += 1
    count.save()
    return JsonResponse({"study_time":count.time_spent})

