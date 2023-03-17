from django.db import models
from django_celery_beat.models import PeriodicTask, IntervalSchedule
# from .tasks import delete_file

# Create your models here.
class Task(models.Model):
    video_url = models.URLField()
    status = models.CharField(max_length=10, default='Pending')
    progress = models.FloatField(default=0.0)
    video_link = models.CharField(max_length=500, blank=True)
    error_message = models.CharField(max_length=500, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)


class FileCleanupTask(PeriodicTask):
    interval = IntervalSchedule(every=2, period='minutes')
    name = 'File cleanup task'
    task = 'myapp.tasks.delete_file'
    # args = ('/path/to/my/file.txt',)

    def save(self, *args, **kwargs):
        if not self.pk and self.enabled:
            self.schedule = self.interval
        return super(FileCleanupTask, self).save(*args, **kwargs)