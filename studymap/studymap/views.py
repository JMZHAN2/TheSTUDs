# studymap/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    return HttpResponse("Welcome to the home page")

def about(request):
    return HttpResponse("This is the about page")


