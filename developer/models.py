from django.contrib.auth.models import AbstractUser
from django.db import models

class Developer(AbstractUser):
    ava_image = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png')
    date_joined_to_work = models.DateField()
    level = models.IntegerField(choices=((1, 'Junior'),(2, 'Middle'), (3, 'Senior'), (4, 'Team lead')), default=1)