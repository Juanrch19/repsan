# Generated by Django 4.2.6 on 2023-12-20 17:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositorio', '0016_alter_categoria_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 20, 12, 4, 43)),
        ),
        migrations.AlterField(
            model_name='document',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 20, 12, 4, 43)),
        ),
        migrations.AlterField(
            model_name='document',
            name='numero_autoincrementable',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='proceso',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 20, 12, 4, 43)),
        ),
    ]
