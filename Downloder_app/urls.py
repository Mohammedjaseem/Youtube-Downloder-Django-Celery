
from django.urls import path, include
from . import views

urlpatterns = [
    path('CheckRadis', views.checkradis, name="CheckRadis"),
    path('', views.add_task, name='add_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('list', views.task_list, name='task_list'),
]