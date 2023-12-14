# Generated by Django 4.2.6 on 2023-12-14 16:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositorio', '0013_document_numero_autoincrementable_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='numero_autoincrementable',
        ),
        migrations.AlterField(
            model_name='categoria',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 14, 11, 23, 36)),
        ),
        migrations.AlterField(
            model_name='document',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 14, 11, 23, 36)),
        ),
        migrations.AlterField(
            model_name='proceso',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 14, 11, 23, 36)),
        ),
    ]
