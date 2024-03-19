import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    ava_image = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png')
    bin = models.CharField(verbose_name='БИН Компании', max_length=30)
    name = models.CharField( verbose_name='Название Компании', max_length=255)
    role = models.IntegerField(choices=((1, 'Developer'),(2, 'Manager'),(3, 'Tester'),(4, 'Analyst')), default=1)
    company_identifier = models.CharField(verbose_name='Идентификатор Компании', max_length=255)

class Level(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level_developer = models.IntegerField(choices=((1, 'Junior'),(2, 'Middle'),(3, 'Senior'),(4, 'Team lead')), default=1)
    level_tester = models.IntegerField(choices=((1, 'Developer'),(2, 'Company'),(3, 'Tester'),(4, 'Analyst')), default=1)




