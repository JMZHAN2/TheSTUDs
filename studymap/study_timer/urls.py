from django.urls import path

from . import views

urlpatterns = [
    path("", views.study_time, name="study_time"),
]