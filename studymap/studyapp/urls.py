from django.contrib import admin
from django.urls import path,include
from . import views
from .views import register


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', register, name='register'),
]

