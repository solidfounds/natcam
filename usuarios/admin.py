from django.contrib import admin

# Register your models here.
from usuarios.models import Sucursal, Datos, GatosSucursal


@admin.register(Sucursal)
class CusursalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'color')
    pass

@admin.register(Datos)
class DatosAdmin(admin.ModelAdmin):
    list_display = ('id','usuario','tipo', 'sucursal')
    filter = ('tipo')
    pass

@admin.register(GatosSucursal)
class GastosSucursal(admin.ModelAdmin):
    pass