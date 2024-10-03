from django.urls import path
from .views import study_time, get_count  # Import the views

urlpatterns = [
    path('', study_time, name='study_time'),  # Home page displaying the timer
    path('get-count/', get_count, name='get_count'),  # Endpoint to increment study time
]
