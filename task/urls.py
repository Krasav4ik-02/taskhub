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
]