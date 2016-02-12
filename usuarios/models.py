from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Sucursal(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    telefono = models.SmallIntegerField()
    renta = models.DecimalField(max_digits=7, decimal_places=2)
    luz = models.DecimalField(max_digits=7, decimal_places=2)
    agua = models.DecimalField(max_digits=7, decimal_places=2)
    varios = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Sucursales'

    def __str__(self):
        return self.nombre

PORCENTAJE_GANANCIA_CHOICES = (
    ('3', '3%'),
    ('4', '4%'),
    ('5', '5%'),
    ('6', '6%'),
)
PERSONAL_CHOICES = (
    ('1', 'Asesor'),
    ('2', 'Asistente'),
)

class Datos(models.Model):
    usuario = models.ForeignKey(User)
    tipo = models.CharField(max_length=2, choices=PERSONAL_CHOICES)
    porcentaje_ganancia = models.CharField(max_length=1, choices=PORCENTAJE_GANANCIA_CHOICES)
    sucursal = models.ForeignKey(Sucursal, blank=True, null=True)
    clave = models.CharField(max_length =10)
    num_de_cuenta = models.CharField(max_length=20)
    banco = models.CharField(max_length=50)

    def __str__(self):
        return self.usuario.username
