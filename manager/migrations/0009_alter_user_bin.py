# Generated by Django 3.2.19 on 2024-04-11 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_auto_20240410_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bin',
            field=models.IntegerField(verbose_name='БИН Компании'),
        ),
    ]
