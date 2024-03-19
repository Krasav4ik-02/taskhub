from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('task.urls')),
    path('', include('vacation.urls')),
    path('', include('manager.urls')),
    path('', include('developer.urls')),
    path('', include('analyst.urls')),
    path('', include('tester.urls')),
]