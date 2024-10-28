from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Stopwatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_spent = models.IntegerField(default=0)
    time_start = models.DateTimeField(default = timezone.now)
    title = models.CharField(max_length=40)
    def __str__(self):
        return f"{self.title}: {self.time_spent} seconds"
    def get_duration(self):
        hours = self.time_spent // 3600
        minutes = (self.time_spent % 3600) // 60
        seconds = self.time_spent % 60
        return {'hours': hours, 'minutes': minutes, 'seconds': seconds}
    
    @staticmethod
    def calculate_study_streak(user):
        # retrieve all study sessions and order by start time
        sessions = Stopwatch.objects.filter(user=user).order_by('-time_start')
        unique_study_dates = set()  # Track unique study dates
        streak = 0
        last_study_date = None
        for session in sessions:
            study_date = session.time_start.date()
            if study_date not in unique_study_dates:
                unique_study_dates.add(study_date)
                if last_study_date is None or (last_study_date - study_date).days == 1:
                    streak += 1
                    last_study_date = study_date
                else:
                    break  # stop counting if there's a gap
        return streak
        





