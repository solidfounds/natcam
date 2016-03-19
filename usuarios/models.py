from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Sucursal(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    telefono = models.SmallIntegerField()
    color = models.CharField(max_length=6, default='#2FCC71')

    class Meta:
        verbose_name_plural = 'Sucursales'

    def __str__(self):
        return self.nombre

class GatosSucursal(models.Model):
    sucursal = models.ForeignKey(Sucursal)
    renta = models.PositiveIntegerField(null=True)
    telefono = models.PositiveIntegerField(null=True)
    luz = models.PositiveIntegerField(null=True, blank=True)
    agua = models.PositiveIntegerField(null=True, blank=True)
    varios = models.PositiveIntegerField(null=True)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.sucursal.nombre

PORCENTAJE_GANANCIA_CHOICES = (
    ('0', '0%'),
    ('1', '1%'),
    ('2', '2%'),
    ('3', '3%'),
    ('4', '4%'),
    ('5', '5%'),
    ('6', '6%'),
)
PERSONAL_CHOICES = (
    ('1', 'Asesor'),
    ('2', 'Asistente'),
    ('3', 'Gael'),
)

class Datos(models.Model):
    usuario = models.ForeignKey(User)
    tipo = models.CharField(max_length=2, choices=PERSONAL_CHOICES)
    porcentaje_ganancia = models.CharField(max_length=1, choices=PORCENTAJE_GANANCIA_CHOICES)
    sucursal = models.ForeignKey(Sucursal, blank=True, null=True)
    claveinterb = models.CharField('Clave Interbancaria',max_length =18)
    num_de_cuenta = models.CharField(max_length=16)
    banco = models.CharField(max_length=50)

    def __str__(self):
        return self.usuario.username
