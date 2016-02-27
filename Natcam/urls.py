"""Natcam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include
from django.contrib import admin
from django.conf.urls import patterns, url
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
      url(r'^home', views.primerRegistro, name='agregar_clientes'),

    #ASESOR



    #ASISTENTE
    url(r'^editar/primer_registro/(?P<pk>\d+)', views.PrimerRegistroEdit, name='editar_primer_registro'),
    url(r'^eliminar/(?P<pk>\d+)$', views.PrimerRegistroDelete, name='eliminar_primer_registro'),
    url(r'^clientes/', views.clientes, name='clientes'),
    url(r'^desempeno/', views.desempeno, name='desempeno'),

    url(r'^$', 'django.contrib.auth.views.login', name='login'),
    url(r'^account/', include('usuarios.urls')),


    url(r'^odc1/(?P<cliente_id>\d+)/', views.orden_compra1, name='odc1'),
    url(r'^odc2/(?P<cliente_id>\d+)/', views.orden_compra2, name='odc2'),
    url(r'^odc3/(?P<cliente_id>\d+)/', views.orden_compra3, name='odc3'),
    url(r'^segundo_registro/$', views.segundoRegistro, name='segundo_registro'),


    url(r'^editar/segundo_registro/(?P<pk>\d+)', views.SegundoRegistroEdit, name='editar_segundo_registro'),
    url(r'^eliminar/(?P<pk>\d+)$', views.SegundoRegistroDelete, name='eliminar_segundo_registro'),
    url(r'^(?P<cliente_id>\d+)$', views.enviar_email, name='enviar_email'),
    url(r'^calendario/$', views.calendario, name='calendario'),

    url(r'^calendario/mes/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',views.dia, name='post_detail'),

    #cargar pdfs
    url(r'^cargar_pds/(?P<id>\d+)', views.cargar_pdfs, name='cargar_pdfs'),
    url(r'^cliente/perfil/(?P<id>\d+)', views.cliente_perfil, name='cliente_perfil'),
    url(r'^gael/admin/(?P<id>\d+)', views.empleado_perfil, name='empleado_perfil'),
    url(r'^gael/admin/sucursales/', views.sucursales, name='sucursales'),
    url(r'^gael/admin/sucursal/(?P<pk>\d+)/$', views.sucursal_unica, name='sucursal_unica'),
    url(r'^gael/admin/comisiones/$', views.comisiones_admingael, name='comisiones_admingael'),

    #asistente
    url(r'^gastos_oficina/', views.gastos_oficina, name='gastos_oficina'),
    url(r'^ver_resumencom/fecha/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.ver_resumencom, name='ver_resumencom'),
]


from django.conf import settings

# ... your normal urlpatterns here
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})


        )