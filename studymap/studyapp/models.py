from django.db import models

# Create your models here.
class Stopwatch(models.Model):
    time_spent = models.IntegerField(default=0)
    time_start = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=40)
    
    
    def __str__(self):
        return f"{self.time_spent}"