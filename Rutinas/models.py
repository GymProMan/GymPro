from cloudinary.models import CloudinaryField

from Miembros.models import Miembro
from Aparatos.models import Aparato
from django.db import models


class Ejercicios(models.Model):
    id_ejercicio = models.AutoField(primary_key=True)
    id_aparato = models.ForeignKey('Aparatos.Aparato', on_delete=models.CASCADE)
    categoria = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100, blank=False, null=False, default='Ejercicio')
    tipo = models.CharField(max_length=100)
    ejecucion = models.TextField()
    guia= models.TextField(null=True)
    foto = models.ImageField(upload_to="ejercicios",null=True)
    foto_cloud = CloudinaryField( 'imagen', folder='general/ejercicios', null=True, blank=True)

    def __str__(self):
        return self.nombre



class Rutina(models.Model):
    id_rutina = models.AutoField(primary_key=True)
    id_miembro = models.ForeignKey('Miembros.Miembro', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    objetivo = models.CharField(max_length=200)
    nota = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    @staticmethod
    def obtener_id_rutina(miembro):
        return Rutina.objects.get(id_miembro=miembro.id)




class RutinaEjercicio(models.Model):
    id_rutina_ejercicio = models.AutoField(primary_key=True)
    id_rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    id_ejercicio = models.ForeignKey(Ejercicios, on_delete=models.CASCADE)
    dia = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100,default='')
    series = models.CharField(max_length=20)
    repeticiones = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id_rutina} - {self.id_ejercicio}"


    @staticmethod
    def obtener_ejercicios_home(rutina):
        ejercicios_por_dia = {dia: [] for dia in
                              ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]}
        ejercicios_rutina = RutinaEjercicio.objects.filter(id_rutina=rutina)
        for ejercicio in ejercicios_rutina:
            if ejercicio.dia in ejercicios_por_dia:
                ejercicios_por_dia[ejercicio.dia].append({
                    "nombre": ejercicio.id_ejercicio.nombre,
                    "categoria":ejercicio.id_ejercicio.categoria,
                    "foto": ejercicio.id_ejercicio.foto_cloud.url,
                })
        return ejercicios_por_dia

    @staticmethod
    def obtener_ejercicios(rutina):
        ejercicios_por_dia = {dia: [] for dia in
                              ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]}
        ejercicios_rutina = RutinaEjercicio.objects.filter(id_rutina=rutina)
        for ejercicio in ejercicios_rutina:
            if ejercicio.dia in ejercicios_por_dia:
                ejercicios_por_dia[ejercicio.dia].append({
                    "foto": ejercicio.id_ejercicio.foto_cloud.url,
                    "nombre": ejercicio.id_ejercicio.nombre,
                    "series": ejercicio.series,
                    "repeticiones": ejercicio.repeticiones,
                })
        return ejercicios_por_dia
