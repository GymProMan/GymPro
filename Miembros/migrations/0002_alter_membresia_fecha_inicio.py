# Generated by Django 5.1.3 on 2024-12-06 15:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Miembros', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membresia',
            name='fecha_inicio',
            field=models.DateField(default=datetime.datetime(2024, 12, 6, 15, 47, 49, 672840, tzinfo=datetime.timezone.utc)),
        ),
    ]
