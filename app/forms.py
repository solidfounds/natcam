# -*- encoding: utf-8 -*-
from .models import PrimerRegistro, SegundoRegistro, Order, RelacionP, CargarPdfs
from django import forms
from django.forms import ModelForm

class PrimerRegistroFORM(ModelForm):
    class Meta:
        model = PrimerRegistro
        fields = ('nombre', 'apellidos', 'calle','numero','colonia_fraccionamiento','municipio_delegacion','endidad','cp', 'nss','telefono','empresa','registro_patronal','comision','numero_de_cuenta','banco')
        #exclude = ['operador_que_lo_registro',]
        widgets={
            'nombre': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm  col-md-2'}),
            'apellidos': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm  col-md-2'}),
            'calle': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm'}),
            'numero': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm'}),
            'colonia_fraccionamiento': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm'}),
            'municipio_delegacion': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm'}),
            'endidad': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm'}),
            'cp': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm'}),
            'nss': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm','min':'8', 'max':"10"}),
            'telefono': forms.TextInput(attrs={'type':'number','required':'true','class':'form-control form-control-sm','placeholder':'Lada - digitos', 'max':"9999000000"}),
            'empresa': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm','placeholder':'Nombre de la empresa'}),
            'registro_patronal': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm','placeholder':'Número de registro patronal'}),
            'comision': forms.TextInput(attrs={'type':'number','required':'true','class':'form-control form-control-sm','placeholder':'Ejemplo: 15000.00','max':"50000"}),
            'email': forms.EmailInput(attrs={'type':'email','required':'true','class':'form-control form-control-sm','placeholder':'ejemplo@hotmail.com'}),
            'numero_de_cuenta': forms.TextInput(attrs={'type':'number','required':'true','class':'form-control form-control-sm','placeholder':'ejemplo: 4465-5487-5986-3215', 'max':"9999999999999999"}),
            'banco': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm'}),

        }


class SegundoRegistroForm(forms.Form):
    cliente = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly':'readonly'}))
    ife = forms.FileField()
    caratula = forms.FileField()
    tarjeta_de_mejoravit = forms.FileField()
    credito = forms.IntegerField()

class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'id', 'total_amount')
        fields = ('orden_compra',)

class EmailOdcsForm(forms.Form):
    to = forms.EmailField(label='Destinatario')
    comments = forms.CharField(label='Comentario',required=False, widget=forms.Textarea(attrs={'rows':'5', 'cols':'50'}))
    url_archivos = forms.URLField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'50'}))
    # ord1 = forms.CharField(widget=forms.TextInput(attrs={"type":'hidden', 'value': '{{ foo.total_amount }}'}))
    # ord2 = forms.CharField(widget=forms.TextInput(attrs={"type":'hidden', 'value': '{{foo.total_amount }}'}))
    # ord3 = forms.CharField(widget=forms.TextInput(attrs={}))

class BuscarDiaForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

class PReferenciaForm(forms.Form):
    cliente = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly':'readonly'}))
    ref_pago = forms.CharField(max_length=12)

class PRBoleanPagoForm(forms.Form):
    clienteb = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly':'readonly'}))
    crbd_rpago = forms.BooleanField()

class OdcsPagadasForm(forms.Form):
    clientec = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly':'readonly'}))
    odc1p = forms.BooleanField()
    odc2p = forms.BooleanField()
    odc3p = forms.BooleanField()


# class RelacionPFprm(ModelForm):
#     class Meta:
#         model = RelacionP
#         fields = ('fecha', 'clien

class CargarPdfsForm(ModelForm):
    class Meta:
        model = CargarPdfs
        fields = ('odc1', 'odc2', 'odc3')