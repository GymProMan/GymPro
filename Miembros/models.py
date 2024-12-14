from datetime import timedelta

import pytz
from cloudinary.models import CloudinaryField
from django.db import models
from django.utils import timezone
from django.utils.timezone import now

from GYM_PRO.settings import TIME_ZONE


# Create your models here.

class MembresiaTipo(models.Model):
    DIAS = 'D'
    SEMANAS = 'S'
    MESES = 'M'
    AÑOS = 'A'

    UNIDADES_TIEMPO = [
        (DIAS, 'Días'),
        (SEMANAS, 'Semanas'),
        (MESES, 'Meses'),
        (AÑOS, 'Años')
    ]

    nombre = models.CharField(max_length=100)
    duracion = models.IntegerField()
    unidad_tiempo = models.CharField(max_length=1, choices=UNIDADES_TIEMPO, default='M')
    beneficios = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Membresia(models.Model):
    miembro = models.ForeignKey('Miembro', on_delete=models.CASCADE)
    tipo_membresia = models.ForeignKey(MembresiaTipo, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=timezone.now())
    fecha_final = models.DateField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if self.tipo_membresia.unidad_tiempo == MembresiaTipo.DIAS:
            self.fecha_final = self.fecha_inicio + timedelta(days=self.tipo_membresia.duracion)
        elif self.tipo_membresia.unidad_tiempo == MembresiaTipo.SEMANAS:
            self.fecha_final = self.fecha_inicio + timedelta(weeks=self.tipo_membresia.duracion)
        elif self.tipo_membresia.unidad_tiempo == MembresiaTipo.MESES:
            self.fecha_final = self.fecha_inicio + timedelta(
                days=30 * self.tipo_membresia.duracion)  # Aproximado 30 días por mes
        elif self.tipo_membresia.unidad_tiempo == MembresiaTipo.AÑOS:
            self.fecha_final = self.fecha_inicio + timedelta(
                days=365 * self.tipo_membresia.duracion)  # Aproximado 365 días por año
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo_membresia.nombre}"

    @staticmethod
    def obtner_membresia_activa(miembro):
        return Membresia.objects.filter(
            miembro=miembro,
            fecha_inicio__lte=now().date()
        ).exclude(
            fecha_final__lt=now().date()
        ).first()

class Miembro(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    clave = models.CharField(max_length=20, unique=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    genero = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    numero_contacto = models.CharField(max_length=15)
    foto = models.ImageField(upload_to='miembros_fotos/', null=True, blank=True)
    foto_cloud = CloudinaryField( 'imagen', folder='general/miembros', null=True, blank=True)


    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def get_username(self):
        return f"{self.nombre} {self.apellido}"

class Asistencia(models.Model):
    miembro = models.ForeignKey('Miembro', on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"Asistencia de {self.miembro.nombre} el {self.fecha} a las {self.hora}"
