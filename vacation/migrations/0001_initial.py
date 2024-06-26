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
            name='VacationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('date', models.DateField()),
                ('comments', models.TextField()),
                ('status', models.IntegerField(choices=[(1, 'На согласований'), (2, 'Одобрено'), (3, 'Отклонено')], default=1)),
                ('type_vacation', models.IntegerField(choices=[(1, 'Оплачиваемый'), (2, 'Социальный'), (3, 'Дополнительный оплачиваемый'), (4, 'Учебный отпуск'), (5, 'Неоплачиваемый')])),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_vacation_requests', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
