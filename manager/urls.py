from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.authentication, name='home'),
    path('registration_manager', views.registration_manager, name='registration_manager'),
    path('authentication', views.authentication, name='authentication'),
    path('registration', views.registration, name='registration'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)