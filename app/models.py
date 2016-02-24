#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class PrimerRegistro(models.Model):
    nombre = models.CharField(max_length=55)
    apellidos = models.CharField(max_length=80)
    calle = models.CharField(max_length=80, null=True)
    numero = models.CharField(max_length=20, null=True)
    colonia_fraccionamiento = models.CharField('Colonia o Fraccionamiento',max_length=200, null=True)
    municipio_delegacion = models.CharField('Municio o Deledación', max_length=200, null=True)
    endidad = models.CharField(max_length=50, null=True)
    cp = models.CharField(max_length=20, null=True)
    nss = models.CharField( 'nss', max_length=11, null=True)
    telefono = models.PositiveIntegerField('teléfono', )
    empresa = models.CharField(max_length=254)
    registro_patronal = models.CharField(max_length=15)
    comision = models.DecimalField('comisión', max_digits=7, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    email = models.EmailField()
    numero_de_cuenta = models.CharField('número de cuenta', max_length=16)
    banco = models.CharField(max_length=15)
    operador = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Primer Registro'

    def __str__(self):
        return "%s, %s" %(self.id, self.nombre )

    def get_absolute_url(self):
        return reverse('editar_primer_registro', kwargs={'pk': self.pk})

def guardar_ife(instance, filename):
    #file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'media/{0}/{1}'.format(instance.cliente, filename)

def guardar_caratula(instance, filename):
    #file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'media/{0}/{1}'.format(instance.cliente, filename)

def guardar_tarjeta(instance, filename):
    #file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'media/{0}/{1}'.format(instance.cliente, filename)

class SegundoRegistro(models.Model):
    cliente = models.ForeignKey(PrimerRegistro)
    fecha = models.DateField(auto_now_add=True)
    ife = models.FileField(upload_to=guardar_ife, blank=True, null=True)
    caratula = models.FileField(upload_to=guardar_caratula, blank=True, null=True)
    tarjeta_de_mejoravit = models.FileField(upload_to=guardar_tarjeta, blank=True, null=True)
    credito = models.DecimalField('crédito', max_digits=7, decimal_places=2, blank=True, null=True)
    operador = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Segundo Registro'
        verbose_name = 'Segundo Registro'

    def __str__(self):
        return self.cliente.nombre

    def get_absolute_url(self):
        return reverse('editar_segundo_registro', kwargs={'pk': self.pk})

    def comisiona(self):
        manoDeObraInfo = (self.credito-(self.credito*20/100))
        iva = (manoDeObraInfo*20/100)
        micomision = (iva*20/100)
        return micomision


# en teoria este es el segundo
class TercerRegistro(models.Model):
    cliente = models.ForeignKey(PrimerRegistro, )
    compra = models.TextField()
    importe_total = models.DecimalField(max_digits=10, decimal_places=2)
    efectivo = models.DecimalField(max_digits=10, decimal_places=2)
    comision = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)
    numero_credito = models.CharField(max_length=10)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Tercer Registro'

    def __str__(self):
        return self.cliente


class Productos(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Productos"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name

ODC_CHOICES = (
    ('1', 'Orden de Compra 1'),
    ('2', 'Orden de Compra 2'),
    ('3', 'Orden de Compra 3'),
)


class Order(models.Model):
    orden_compra = models.CharField('orden de compra',max_length=1,choices=ODC_CHOICES)
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='date')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(PrimerRegistro)
    operador = models.ForeignKey(User)

    def __str__(self):
        return 'Orden No. %i' % self.id

    def get_absolute_url(self):
        return reverse('enviar_email', args=[ self.id,])

class ProductOrder(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Productos)
    quantity = models.IntegerField()

    def importe(self):
        return (self.product.price * self.quantity)


class RelacionP(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    cliente = models.OneToOneField(PrimerRegistro, null=True,)
    odc1 = models.PositiveIntegerField()
    odc1p = models.BooleanField(default=False)
    odc2 = models.PositiveIntegerField(null=True, blank=True)
    odc2p = models.BooleanField(default=False)
    odc3 = models.PositiveIntegerField(null=True, blank=True)
    odc3p = models.BooleanField(default=False)
    pag_clie = models.PositiveIntegerField()
    p_asesor = models.PositiveIntegerField()
    comision = models.PositiveIntegerField()
    com_t = models.PositiveIntegerField()
    asesor = models.ForeignKey(User, null=True)
    ref_pago = models.CharField('Referencia de Pago',max_length=20, null=True, blank=True)
    crbd_rpago = models.BooleanField(default=False)
    importe = models.DecimalField('Importe',max_digits=7, decimal_places=2, null=True)

    # def __str__(self):
    #     return self.fecha
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.fecha.year,
                                                 self.fecha.strftime('%m'),
                                                 self.fecha.strftime('%d'),])

class CargarPdfs(models.Model):
    cliente = models.ForeignKey(PrimerRegistro)
    odc1 = models.FileField(upload_to='cargarpdfs/')
    odc2 = models.FileField(upload_to='cargarpdfs/', blank=True, null=True)
    odc3 = models.FileField(upload_to='cargarpdfs/', blank=True, null=True)
    operador = models.ForeignKey(User)