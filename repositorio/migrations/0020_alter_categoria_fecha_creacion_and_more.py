# Generated by Django 4.2.6 on 2024-02-05 16:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repositorio', '0019_rename_perfil_userprofile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 5, 11, 34, 30)),
        ),
        migrations.AlterField(
            model_name='document',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 5, 11, 34, 30)),
        ),
        migrations.AlterField(
            model_name='proceso',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 5, 11, 34, 30)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
