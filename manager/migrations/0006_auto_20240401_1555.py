# Generated by Django 3.2.19 on 2024-04-01 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_auto_20240401_0143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='company_identifier',
        ),
        migrations.AlterField(
            model_name='user',
            name='bin',
            field=models.CharField(max_length=12, verbose_name='БИН Компании'),
        ),
        migrations.AlterField(
            model_name='user',
            name='data_joined_to_work',
            field=models.DateField(),
        ),
    ]