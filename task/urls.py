from django.urls import path
from . import views

urlpatterns = [
    path('create_project', views.create_project, name='create_project'),
    path('create_task', views.create_task, name='create_task'),
    path('edit_task', views.edit_task, name='edit_task'),
    path('edit_project', views.edit_project, name='edit_project'),
    path('send_task', views.send_task, name='send_task'),
    path('get_info_users', views.get_info_users, name='get_info_users'),
    path('calculate_user_kpi', views.calculate_user_kpi, name='calculate_user_kpi'),
    path('edit_user', views.edit_user, name='edit_user'),
    path('dissmiss', views.dissmiss, name='dismiss'),
    path('link_developer', views.link_developer, name='link_developer'),
    path('invite_task', views.invite_task, name='invite_task'),
    path('freeze_task', views.freeze_task, name='freeze_task'),
    path('completed_task', views.completed_task, name='completed_task'),
    path('send_task_analyst', views.send_task_analyst, name='send_task_analyst'),
    path('send_modification', views.send_modification, name='send_modification'),
]