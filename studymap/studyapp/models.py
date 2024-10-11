from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stopwatch(models.Model):
    time_spent = models.IntegerField(default=0)
    time_start = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=40)
    
    
    def __str__(self):
        return f"{self.time_spent}"

class StudyStreak(models.Model):
    users = models.ForeignKey(User, on_delete = models.CASCADE)
    streak_days = models.PositiveIntegerField(default=0)  
    start_date = models.DateField(null=True, blank=True) 
    last_study_date = models.DateField(null=True, blank=True)  

    def __str__(self):
        return f"{self.user.username} - Streak: {self.streak_days} days"