# Generated by Django 4.2.6 on 2023-12-01 19:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repositorio', '0006_alter_categoria_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proceso',
            fields=[
                ('id_proceso', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_proceso', models.CharField(max_length=100, verbose_name='nombre_proceso')),
                ('fecha_creacion', models.DateTimeField(default=datetime.datetime(2023, 12, 1, 14, 31, 3))),
            ],
        ),
        migrations.AlterField(
            model_name='categoria',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 1, 14, 31, 3)),
        ),
        migrations.AlterField(
            model_name='codigo',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 1, 14, 31, 3)),
        ),
        migrations.AlterField(
            model_name='document',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 1, 14, 31, 3)),
        ),
        migrations.AddField(
            model_name='document',
            name='proceso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='repositorio.proceso', verbose_name='Proceso'),
        ),
    ]
