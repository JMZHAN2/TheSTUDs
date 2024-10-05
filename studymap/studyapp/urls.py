from django.contrib import admin
from django.urls import path,include
from . import views
from .views import register, study_time, update_time


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('timer/', views.study_time, name='study_timer'),
]

