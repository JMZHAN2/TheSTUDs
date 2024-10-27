from django.contrib import admin
from django.urls import path,include
from . import views
from .views import register, study_time, finish_session


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('timer/', views.study_time, name='study_timer'),
    path('finish-session/', finish_session, name='finish_session'),
]

