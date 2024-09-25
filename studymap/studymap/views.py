# studymap/views.py
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the home page")

def about(request):
    return HttpResponse("This is the about page")