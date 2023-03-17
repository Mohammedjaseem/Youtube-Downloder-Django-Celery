from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task
from .tasks import  download_video_task
from pytube import YouTube
from django.http import FileResponse
from django.conf import settings
import os
# Create your views here.

#checking radis connection
import redis
def checkradis(request):
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    r.set('foo', 'bar')
    value = r.get('foo')
    print(value)
    return HttpResponse(value)


#task functions start here
def add_task(request):
    if request.method == 'POST':
        # video_url = 
        download_video_task.delay(request.POST['video_url'])
        return redirect('task_list')
    return render(request, 'add_task.html')


def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('task_list')

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})





