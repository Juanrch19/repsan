# Generated by Django 4.2.6 on 2023-11-29 21:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repositorio', '0004_alter_categoria_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 29, 16, 2, 1)),
        ),
        migrations.AlterField(
            model_name='codigo',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 29, 16, 2, 1)),
        ),
        migrations.AlterField(
            model_name='document',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='repositorio.categoria', verbose_name='Categoría'),
        ),
        migrations.AlterField(
            model_name='document',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 29, 16, 2, 1)),
        ),
    ]
