from django.db import models

# Create your models here.
class Aparato(models.Model):
    idAparatos=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=80)
    cantidad = models.IntegerField()
    bandera= models.BooleanField()
    tipo = models.CharField(max_length=50)
    ubicacion=models.CharField(max_length=50)
    estado=models.BooleanField()

    def __str__(self):
            return self.nombre



class CategoriaAparato(models.Model):
    idCategoria=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class CategoriaApa_Aparato(models.Model):
    idCategoria=models.ForeignKey(CategoriaAparato,on_delete=models.CASCADE)
    idAparato=models.ForeignKey(Aparato,on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.idCategoria} {self.idAparato}"
