# Generated by Django 5.1.3 on 2024-12-13 02:38

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Rutinas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ejercicios',
            name='foto_cloud',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='imagen'),
        ),
    ]
