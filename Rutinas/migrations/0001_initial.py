# Generated by Django 5.1.3 on 2024-12-08 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Aparatos', '0001_initial'),
        ('Miembros', '0006_alter_membresia_fecha_inicio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ejercicios',
            fields=[
                ('id_ejercicio', models.AutoField(primary_key=True, serialize=False)),
                ('categoria', models.CharField(max_length=100)),
                ('nombre', models.CharField(default='Ejercicio', max_length=100)),
                ('tipo', models.CharField(max_length=100)),
                ('ejecucion', models.TextField()),
                ('guia', models.TextField(null=True)),
                ('foto', models.ImageField(null=True, upload_to='ejercicios')),
                ('id_aparato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aparatos.aparato')),
            ],
        ),
        migrations.CreateModel(
            name='Rutina',
            fields=[
                ('id_rutina', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('objetivo', models.CharField(max_length=200)),
                ('nota', models.TextField(blank=True, null=True)),
                ('id_miembro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Miembros.miembro')),
            ],
        ),
        migrations.CreateModel(
            name='RutinaEjercicio',
            fields=[
                ('id_rutina_ejercicio', models.AutoField(primary_key=True, serialize=False)),
                ('dia', models.CharField(max_length=20)),
                ('nombre', models.CharField(default='', max_length=100)),
                ('series', models.CharField(max_length=20)),
                ('repeticiones', models.CharField(max_length=20)),
                ('id_ejercicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Rutinas.ejercicios')),
                ('id_rutina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Rutinas.rutina')),
            ],
        ),
    ]
