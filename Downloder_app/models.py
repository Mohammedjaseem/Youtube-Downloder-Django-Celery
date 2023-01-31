from django.db import models

# Create your models here.
class Task(models.Model):
    video_url = models.URLField()
    status = models.CharField(max_length=10, default='Pending')
    progress = models.FloatField(default=0.0)