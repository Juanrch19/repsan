# Generated by Django 4.2.6 on 2024-02-05 16:27

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repositorio', '0018_alter_categoria_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Perfil',
            new_name='UserProfile',
        ),
        migrations.AlterField(
            model_name='categoria',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 5, 11, 27, 53)),
        ),
        migrations.AlterField(
            model_name='document',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 5, 11, 27, 53)),
        ),
        migrations.AlterField(
            model_name='proceso',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 5, 11, 27, 53)),
        ),
    ]
