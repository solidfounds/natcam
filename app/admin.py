from django.contrib import admin
from .models import  PrimerRegistro,SegundoRegistro, Productos, Order, ProductOrder, RelacionP


@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    pass

@admin.register(PrimerRegistro)
class PrimerRegistroAdmin(admin.ModelAdmin):
    list_filter = ('empresa',)
    search_fields = ('nombre', 'id', 'nsn', 'registro_patronal', 'email', 'numero_de_cuenta')
    #list_filter = ('operador_que_lo_registro__nombre','fecha')
    pass

@admin.register(SegundoRegistro)
class SegundoRegistroAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha', 'caratula','tarjeta_de_mejoravit','credito', 'operador', 'comisiona')
    list_filter = ('fecha','operador' )
    search_fields = ('caratula', 'cliente')


class ProductInline(admin.TabularInline):
     extra = 1
     model = ProductOrder
     verbose_name = "Productos en esta orden"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInline,]
    list_display = ('__str__', 'order_date', 'orden_compra','total_amount', 'user')
    list_filter = ('order_date','orden_compra','operador__username',)


@admin.register(RelacionP)
class RelacionP(admin.ModelAdmin):
    list_display = ('id','fecha', 'odc1', 'odc2', 'odc3', )
