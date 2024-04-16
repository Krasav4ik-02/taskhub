from django.urls import path
from . import views

urlpatterns = [
    path('home/notifications', views.notifications, name='notifications'),
    path('home/notifications/notification_read', views.mark_notification_as_read, name='notification_read'),
]