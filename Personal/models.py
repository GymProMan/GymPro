from cloudinary.models import CloudinaryField
from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime

class Turno(models.Model):
    id_turno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_final = models.TimeField()

    def __str__(self):
        return f"{self.nombre} ({self.hora_inicio.strftime('%I:%M %p')} - {self.hora_final.strftime('%I:%M %p')})"


class Personal(models.Model):
    id_personal = models.AutoField(primary_key=True)  # Llave primaria
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)  # Llave foránea a Turnos
    clave = models.CharField(max_length=4, unique=True, validators=[RegexValidator(r'^\d{4}$')], blank=True)  # Clave autogenerada
    nombre = models.CharField(max_length=100)  # Nombre del personal
    apellido = models.CharField(max_length=100)  # Apellido del personal
    fecha_inicio = models.DateField()  # Fecha de inicio en la compañía
    puesto = models.CharField(max_length=100)  # Puesto en la compañía
    numero_contacto = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?1?\d{9,15}$')])  # Número de contacto
    foto = models.ImageField(upload_to="personal", blank=True, null=True)
    foto_cloud = CloudinaryField('imagen',folder='general/personal', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - Clave: {self.clave} - Turno: {self.turno.nombre}"

    def save(self, *args, **kwargs):
        if not self.clave:  # Si no hay clave asignada, se genera de forma automática
            last_personal = Personal.objects.all().order_by('id_personal').last()
            if last_personal:
                last_clave = int(last_personal.clave)
                new_clave = f"{last_clave + 1:04d}"
            else:
                new_clave = "0001"
            self.clave = new_clave

        # Ruta de la foto: guardarla como cadena personalizada
        if not self.foto:  # Asignar ruta si no está definida
            self.foto = f"personal_fotos/{self.nombre.lower()}_{self.apellido.lower()}_{datetime.now().strftime('%Y%m%d')}.jpg"

        super().save(*args, **kwargs)

class Asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True)  # Llave primaria
    personal = models.ForeignKey('Personal', on_delete=models.CASCADE)  # Llave foránea a Personal
    fecha = models.DateField()  # Fecha de la asistencia
    hora_entrada = models.TimeField()  # Hora de entrada
    hora_salida = models.TimeField(null=True, blank=True)  # Hora de salida (puede estar en blanco si el empleado aún no ha salido)

    def __str__(self):
        return f"Asistencia de {self.personal.nombre} {self.personal.apellido} el {self.fecha}"

    def marcar_salida(self):
        """Método para registrar la hora de salida."""
        self.hora_salida = datetime.now().time()
        self.save()
