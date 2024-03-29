# Generated by Django 4.2.6 on 2024-02-13 20:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositorio', '0024_alter_categoria_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 13, 15, 24, 54)),
        ),
        migrations.AlterField(
            model_name='document',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 13, 15, 24, 54)),
        ),
        migrations.AlterField(
            model_name='glosario',
            name='definicion',
            field=models.TextField(max_length=1000, verbose_name='definicion'),
        ),
        migrations.AlterField(
            model_name='proceso',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 13, 15, 24, 54)),
        ),
    ]
