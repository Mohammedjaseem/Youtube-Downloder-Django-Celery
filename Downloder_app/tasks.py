from yt_dlp import YoutubeDL
from celery import shared_task
from .models import Task
import time
import os
import datetime

@shared_task(bind=True)
def download_video_task(self, video_url):
    task = Task()
    task.video_url = video_url
    task.status = 'STARTED'
    task.save()

    try:
        ydl_opts = {
            'outtmpl': f'videos/{task.id}.' + '%(ext)s'
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)

        task.status = 'SUCCESS'
        task.progress = 100.0
        task.error_message = "No error occured"
        task.video_link = 'videos/'+ f'{task.id}' +'.'+info['ext']
        task.save()
        return "Video downloader"

    except Exception as e:
        task.status = 'FAILED'
        task.progress = 0.0
        task.error_message = str(e)
        task.save()
        return "Download Failed"
    
@shared_task
def delete_file():
    print("Calling deleting fuction ########################################################")
    time = datetime.datetime.now() - datetime.timedelta(minutes=1)
    datas = Task.objects.filter(created_on__lt=time).exclude(status="DELETED")
    for data in datas:
        try:
            path = os.path.join(os.getcwd(), data.video_link)
            print(f"{path}, #################################")
            os.remove(path)
            data.status = 'DELETED'
            data.error_message = "SUCESS"
            data.save()
            
        except Exception as e:
            data.status = 'DELETING FAILED'
            data.error_message = str(e)
            data.save()

    return "Delete Task Response"



    

    

   
