from django.db import models
from manager.models import User


class Project(models.Model):
    name_project = models.CharField(verbose_name=' Название проекта', max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_descriptions = models.CharField(verbose_name=' Описание', max_length=255)
    project_date_start = models.DateField(verbose_name=' Дата создание')
    project_date_end = models.DateField(verbose_name=' Дата окончания')

class ProjectMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_task = models.CharField(verbose_name='Название задачи', max_length=100)
    task_descriptions = models.CharField(verbose_name=' Описание задачи', max_length=255)
    task_date_start = models.DateTimeField(verbose_name=' Дата создания задачи')
    task_date_end = models.DateTimeField(verbose_name=' Дата окончания задачи')
    task_priority = models.IntegerField(choices=(
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'normal'),
        (4, 'medium'),
        (5, 'High')
        ), default=1)
    task_complexity = models.IntegerField(choices=(
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'normal'),
        (4, 'medium'),
        (5, 'High')),
        default=1)
    task_status = models.IntegerField(choices=(
        (1, 'На разработке'),
        (2, 'На проверке'),
        (3, 'На доработке '),
        (4, 'У аналитика на проверке'),
        (5, 'Выполнено'),
        ),default=1)
    id_tester = models.IntegerField(null=True)
