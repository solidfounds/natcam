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

from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf.urls import patterns, url
from app import views
from usuarios.views import user_login

urlpatterns = [
    url(r'^admin/', admin.site.urls),
      url(r'^home', 'app.views.primerRegistro', name='agregar_clientes'),
    url(r'^editar/primer_registro/(?P<pk>\d+)', views.PrimerRegistroEdit, name='editar_primer_registro'),
    url(r'^eliminar/(?P<pk>\d+)$', views.PrimerRegistroDelete, name='eliminar_primer_registro'),
    url(r'^clientes/', 'app.views.clientes', name='clientes'),
    url(r'^desempeno/', 'app.views.desempeno', name='desempeno'),

    url(r'^$', 'django.contrib.auth.views.login', name='login'),
    url(r'^account/', include('usuarios.urls')),

    #url(r'^$', userlogin.as_view(), name='login'),
    #url(r'^$', 'users.views.userlogin', name='login'),
    #url(r'^salir/$', 'users.views.LogOut', name='logout'),
    url(r'^odc1/(?P<cliente_id>\d+)/', views.orden_compra1, name='odc1'),
    url(r'^odc2/(?P<cliente_id>\d+)/', views.orden_compra2, name='odc2'),
    url(r'^odc3/(?P<cliente_id>\d+)/', views.orden_compra3, name='odc3'),
    url(r'^segundo_registro/$', views.segundoRegistro, name='segundo_registro'),
    # url(r'^detail/(?P<object_id>\d+)/$', 'products.views.detail_view', name='detail_view'),

    url(r'^editar/segundo_registro/(?P<pk>\d+)', views.SegundoRegistroEdit, name='editar_segundo_registro'),
    url(r'^eliminar/(?P<pk>\d+)$', views.SegundoRegistroDelete, name='eliminar_segundo_registro'),
    url(r'^(?P<cliente_id>\d+)$', views.enviar_email, name='enviar_email'),
    url(r'^calendario/$', views.calendario, name='calendario'),

    url(r'^dia/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',views.dia, name='post_detail'),

    #cargar pdfs
    url(r'^cargar_pds/(?P<id>\d+)', views.cargar_pdfs, name='cargar_pdfs'),
    url(r'^cliente/perfil/(?P<id>\d+)', views.cliente_perfil, name='cliente_perfil'),
    url(r'^gael/admin/(?P<id>\d+)', views.empleado_perfil, name='empleado_perfil'),
    url(r'^gael/admin/', views.sucursales, name='sucursales'),

    #asistente
    url(r'^gastos_oficina/', views.gastos_oficina, name='gastos_oficina'),
]


from django.conf import settings

# ... your normal urlpatterns here
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})


        )