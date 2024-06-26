# Generated by Django 3.2.19 on 2024-06-01 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_project', models.CharField(max_length=100, verbose_name=' Название проекта')),
                ('project_descriptions', models.CharField(max_length=255, verbose_name=' Описание')),
                ('project_date_start', models.DateField(verbose_name=' Дата создание')),
                ('project_date_end', models.DateField(verbose_name=' Дата окончания')),
                ('file_project', models.FileField(default='', null=True, upload_to='project_files/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_task', models.CharField(max_length=100, verbose_name='Название задачи')),
                ('task_descriptions', models.CharField(max_length=255, verbose_name=' Описание задачи')),
                ('task_date_start', models.DateField(verbose_name=' Дата создания задачи')),
                ('task_date_end', models.DateField(verbose_name=' Дата окончания задачи')),
                ('task_priority', models.IntegerField(choices=[(1, 'Very Low'), (2, 'Low'), (3, 'normal'), (4, 'medium'), (5, 'High')], default=1)),
                ('task_complexity', models.IntegerField(choices=[(1, 'Very Low'), (2, 'Low'), (3, 'normal'), (4, 'medium'), (5, 'High')], default=1)),
                ('task_status', models.IntegerField(choices=[(1, 'На разработке'), (2, 'На проверке'), (3, 'На доработке '), (4, 'У аналитика на проверке'), (5, 'Выполнено'), (6, 'Заморожен')], default=1)),
                ('task_vacation_status', models.BooleanField(default=False)),
                ('id_tester', models.IntegerField(null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_task', models.FileField(default='', null=True, upload_to='task_files/')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Комментарии')),
                ('action', models.IntegerField(choices=[(1, 'Create task'), (2, 'Send tester'), (3, 'Send modification'), (4, 'Send analyst'), (5, 'Link developer')], default=1)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='task.task')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[(1, 'Manager'), (2, 'Developer Junior'), (3, 'Developer Middle'), (4, 'Developer Senior'), (5, 'Developer Teamlead'), (6, 'Tester'), (7, 'Analyst'), (8, 'Main Analyst')], default=1)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_project', models.FileField(default='', null=True, upload_to='project_files/')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='task.project')),
            ],
        ),
    ]
