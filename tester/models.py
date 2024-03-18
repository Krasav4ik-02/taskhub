from django.contrib.auth.models import AbstractUser
from django.db import models

class Tester(AbstractUser):
    ava_image = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png')
    company_identifier = models.CharField(verbose_name='Идентификатор Компании', max_length=255)
    date_joined_to_work = models.DateField()
    level = models.IntegerField(choices=((1, 'Главный тестировщик'),(2, 'Тестировщик')), default=2)
