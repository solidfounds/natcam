from django.contrib import admin

# Register your models here.
from usuarios.models import Sucursal, Datos


@admin.register(Sucursal)
class CusursalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'color')
    pass

@admin.register(Datos)
class DatosAdmin(admin.ModelAdmin):
    pass