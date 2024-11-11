from django.contrib import admin
from django.urls import path,include
from . import views
from .views import register, study_time, finish_session, study_statistics

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('timer/', views.study_time, name='study_timer'),
    path('finish-session/', finish_session, name='finish_session'),
    path('study-statistics/', study_statistics, name='study_statistics'),
]

#####Study Streak Visualization
from django.urls import path
from . import views

urlpatterns = [
    path('study-report/', views.study_report_view, name='study_report'),
]
###########
