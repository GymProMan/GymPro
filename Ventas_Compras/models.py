from django.contrib.auth.models import User
from django.db import models

from Miembros.models import MembresiaTipo


# Create your models here.

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=500)
    costo = models.FloatField(default=0)
    precio = models.FloatField(default=0)
    existencias = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='products/', null=True, blank=True)
    estado = models.IntegerField(default=1, editable=False)

    def __str__(self):
        return self.Nombre

class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    nombre_empresa = models.CharField(max_length=30)
    direccion = models.CharField(max_length=30)
    colonia = models.CharField(max_length=30)
    ciudad = models.CharField(max_length=30)
    telefono = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.nombre_empresa}"

class Compras(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra {self.id} - Proveedor: {self.proveedor.nombre}, Total: {self.total}"

class Compras_Producto(models.Model):
    compra = models.ForeignKey(Compras, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_productos = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad_productos}x {self.producto.nombre} en compra {self.compra.id}"

    def get_subtotal(self):
        return self.producto.precio * self.cantidad_productos

class Ventas(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pom = models.CharField(max_length=15)

    def __str__(self):
        return f"Venta {self.id}, Total: {self.total}"

class Ventas_Producto(models.Model):
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_productos = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad_productos}x {self.producto.nombre} en compra {self.venta.id}"

    def get_subtotal(self):
        return self.producto.precio * self.cantidad_productos

class Ventas_Membresias(models.Model):
    membresia = models.ForeignKey(MembresiaTipo, on_delete=models.CASCADE)
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)