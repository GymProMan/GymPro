# Generated by Django 5.1.3 on 2024-12-08 14:28

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id_personal', models.AutoField(primary_key=True, serialize=False)),
                ('clave', models.CharField(blank=True, max_length=4, unique=True, validators=[django.core.validators.RegexValidator('^\\d{4}$')])),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('fecha_inicio', models.DateField()),
                ('puesto', models.CharField(max_length=100)),
                ('numero_contacto', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$')])),
                ('foto', models.ImageField(blank=True, null=True, upload_to='personal')),
            ],
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id_turno', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('hora_inicio', models.TimeField()),
                ('hora_final', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id_asistencia', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('hora_entrada', models.TimeField()),
                ('hora_salida', models.TimeField(blank=True, null=True)),
                ('personal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Personal.personal')),
            ],
        ),
        migrations.AddField(
            model_name='personal',
            name='turno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Personal.turno'),
        ),
    ]
