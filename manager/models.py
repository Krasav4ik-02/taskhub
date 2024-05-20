from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ava_image = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png')
    bin = models.CharField(verbose_name='БИН Компании', max_length=12, null=False)
    name_company = models.CharField( verbose_name='Название Компании', max_length=255, null=False)
    role = models.IntegerField(choices=((1, 'Manager'),
                                        (2, 'Developer Junior'),
                                        (3, 'Developer Middle'),
                                        (4, 'Developer Senior'),
                                        (5, 'Developer Teamlead'),
                                        (6, 'Tester'),
                                        (7, 'Analyst'),
                                        (8, 'Main Analyst')), default=1, null=False)
    data_joined_to_work = models.DateField(null=True)
    country = models.CharField( max_length=30, null=True)
    telegram = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    phone_number = models.CharField(max_length=30, null=True)
    task_norm = models.IntegerField(default=0)  # Норма задач для разработчика
    task_plan = models.IntegerField(default=0)  # План задач для разработчика
    task_goal = models.IntegerField(default=0)

class Company(models.Model):
    bin = models.ForeignKey(User, on_delete=models.CASCADE)
    descriptions = models.TextField(verbose_name=' Описание компаний')
    email = models.CharField(verbose_name='Электронная почта', max_length=30)
    address = models.CharField(verbose_name=' Адрес', max_length=30)
    contact_phone = models.CharField(verbose_name=' Контактные данные', max_length=30)
    telegram = models.CharField(verbose_name='Телеграмм', max_length=30)