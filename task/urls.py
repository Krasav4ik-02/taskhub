from django.urls import path
from . import views

urlpatterns = [
    path('create_project', views.create_project, name='create_project'),
    path('create_task', views.create_task, name='create_task'),
    path('edit_task', views.edit_task, name='edit_task'),
    path('edit_project', views.edit_project, name='edit_project'),
    path('send_task', views.send_task, name='send_task'),
]