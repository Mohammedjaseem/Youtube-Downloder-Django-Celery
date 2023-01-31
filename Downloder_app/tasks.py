from pytube import YouTube
from celery import shared_task
from .models import Task


@shared_task(bind=True)
def download_video_task(self, video_url):
    task = Task()
    task.video_url = video_url
    task.status = 'STARTED'
    task.save()

    yt = YouTube(video_url)
    video = yt.streams.first()
    video.download()

    task.status = 'SUCCESS'
    task.progress = 100.0
    task.save()

    return "Video Downloaded"