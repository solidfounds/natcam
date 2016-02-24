from itertools import chain
import json
import datetime

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.utils import timezone
from django.contrib.auth.models import User

from .forms import PrimerRegistroFORM, SegundoRegistroForm, OrderForm, EmailOdcsForm, CargarPdfsForm,\
    PReferenciaForm,  BuscarDiaForm, PRBoleanPagoForm, OdcsPagadasForm
from .models import PrimerRegistro, SegundoRegistro, Productos, ProductOrder, Order, RelacionP
from usuarios.models import Datos, Sucursal, GatosSucursal
from usuarios.forms import GatosSucursalForm


def index(request):
    return render(request, 'index.html', )



@login_required(login_url='/')
def clientes(request):
    usuario = request.user
    if request.method == 'POST':
        form = SegundoRegistroForm(request.POST, request.FILES)
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            ife = form.cleaned_data['ife']
            caratula = form.cleaned_data['caratula']
            tarjeta = form.cleaned_data['tarjeta_de_mejoravit']
            credito = form.cleaned_data['credito']
            getcliente = PrimerRegistro.objects.get(id = cliente)
            operador = form.operador = getcliente.operador

            ar = SegundoRegistro.objects.create(cliente=getcliente, ife=ife,caratula=caratula, tarjeta_de_mejoravit=tarjeta,credito=credito , operador=operador)
            ar.save()
            return redirect('clientes')
    else:
        form = SegundoRegistroForm()
    datos = Datos.objects.get(usuario=usuario)
    sucursa = datos.sucursal
    asesore = Datos.objects.filter(sucursal=sucursa ).filter(tipo =1)
    cliente = PrimerRegistro.objects.filter(operador__id__in=asesore)
    tarjeta = SegundoRegistro.objects.filter(operador__id__in=asesore)
    ordenes = Order.objects.filter(operador__username__contains=asesore)
    orden1 = Order.objects.filter(Q(orden_compra="1") & Q(operador__id__in=asesore))
    orden2 = Order.objects.filter(Q(orden_compra="2") & Q(operador__id__in=asesore))
    orden3 = Order.objects.filter(Q(orden_compra="3") & Q(operador__id__in=asesore))
    odcs = Order.objects.filter(Q(operador__username__contains=usuario))
    return render(request, 'clientes.html', {
            'cliente': cliente,
            'tarjeta': tarjeta,
            'ordenes': ordenes,
            'orden1': orden1,
            'orden2': orden2,
            'orden3': orden3,
            'odcs': odcs,
            'form':form,
            'datos':datos
        })

#@login_required(login_url='/')
def desempeno(request):
    usuario = request.user
    datos = Datos.objects.get(usuario = usuario)
    if datos.tipo == "1":
        mi_info = User.objects.get(username=usuario)
        total_clientes = PrimerRegistro.objects.filter(operador__username__contains=usuario).count()
        micomision = PrimerRegistro.objects.filter(operador__username__contains=usuario)
        micomiscionAsesor = SegundoRegistro.objects.filter(operador__username__contains=usuario)
        #percepcion = SegundoRegistro.objects.filter(operador__username__contains=usuario).aggregate(Sum('micomision'))
        return render(request, 'asesor/desempeno.html', {'mi_info': mi_info,
                                                  'total_clientes': total_clientes,
                                                  'micomision':micomision,
                                                  'micomiscionAsesor':micomiscionAsesor,
                                                  'datos':datos,
                                                  })
    elif datos.tipo == "2":
        mi_info = User.objects.get(username=usuario)
        total_clientes = PrimerRegistro.objects.filter(operador__username__contains=usuario).count()
        micomision = PrimerRegistro.objects.filter(operador__username__contains=usuario)
        micomiscionAsesor = SegundoRegistro.objects.filter(operador__username__contains=usuario)
        #percepcion = SegundoRegistro.objects.filter(operador__username__contains=usuario).aggregate(Sum('micomision'))
        return render(request, 'asistente/desempeno.html', {'mi_info': mi_info,
                                                  'total_clientes': total_clientes,
                                                  'micomision':micomision,
                                                  'micomiscionAsesor':micomiscionAsesor,
                                                  'datos':datos,
                                                  #'percepcion': percepcion
                                                  })
    elif datos.tipo == "3":
        mi_info = User.objects.get(username=usuario)
        total_clientes = PrimerRegistro.objects.filter(operador__username__contains=usuario).count()
        micomision = PrimerRegistro.objects.filter(operador__username__contains=usuario)
        micomiscionAsesor = SegundoRegistro.objects.filter(operador__username__contains=usuario)
        #percepcion = SegundoRegistro.objects.filter(operador__username__contains=usuario).aggregate(Sum('micomision'))
        com_pgds = RelacionP.objects.all()
        primer_rp = RelacionP.objects.all().first()
        segundo_rp = RelacionP.objects.all().last()
        prm = primer_rp.fecha.month
        lrm = segundo_rp.fecha.month
        pry = primer_rp.fecha.year
        lry = segundo_rp.fecha.year
        sum_relacionpt = RelacionP.objects.all().aggregate(Sum('importe'))
        sum_fact = RelacionP.objects.all().aggregate(Sum('pag_clie'))
        sum_com_t = RelacionP.objects.all().aggregate(Sum('com_t'))
        return render(request, 'gaeladmin/gael-desempeno.html', {'mi_info': mi_info,
                                                  'total_clientes': total_clientes,
                                                  'micomision':micomision,
                                                  'micomiscionAsesor':micomiscionAsesor,
                                                  'datos':datos,
                                                  #'percepcion': percepcion
                                                  'com_pgds':com_pgds,
                                                  'prm':prm,
                                                  'lrm':lrm,
                                                  'pry':pry,
                                                  'lry':lry,
                                                  'sum_relacionpt':sum_relacionpt,
                                                  'sum_fact':sum_fact,
                                                  'sum_com_t':sum_com_t
                                                  })
#@login_required(login_url='/')
def primerRegistro(request):
    operadort = request.user
    datos = Datos.objects.get(usuario__username= operadort)

    if datos.tipo == "1":
        sucursal = datos.sucursal
        asistente = Datos.objects.get(Q(tipo = "2") & Q(sucursal=sucursal) )
        odcs = Order.objects.filter(operador__id=asistente.id)
        datos = Datos.objects.get(usuario = operadort)
        if request.method == 'POST':
            form = PrimerRegistroFORM(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.operador = operadort
                post.save()
                return redirect('agregar_clientes')
        else:
            form = PrimerRegistroFORM()
        mis_clientes = PrimerRegistro.objects.filter(operador__username__contains=operadort)
        return render(request, 'asesor/index.html', {
                                              'form': form,
                                              'mis_clientes': mis_clientes,
                                              'odcs': odcs,
                                               'datos':datos })
    elif datos.tipo == "2":
        return redirect('clientes')
    elif datos.tipo == "3":
        return redirect('calendario')



#@login_required(login_url='/')
def PrimerRegistroEdit(request, pk, template_name='editar/primer_registro.html'):
    clientes = get_object_or_404(PrimerRegistro, pk=pk)
    form = PrimerRegistroFORM(request.POST or None, instance=clientes)
    if form.is_valid():
        form.save()
        return redirect('agregar_clientes')
    return render(request, template_name, {'form': form})


#@login_required(login_url='/')
def PrimerRegistroDelete(request, pk, template_name='delete/confirmacion.html'):
    clientes = get_object_or_404(PrimerRegistro, pk=pk)
    if request.method == 'POST':
        clientes.delete()
        return redirect('agregar_clientes')
    return render(request, template_name, {'object': clientes})


#@login_required(login_url='/')
def segundoRegistro(request):
    usuario = request.user
    if request.method == 'POST':
        form = SegundoRegistroForm(request.POST, request.FILES)
        if form.is_valid():
            posta = form.save(commit=False)
            posta.operador = usuario
            posta.save()
            return redirect('segundo_registro')
    else:
        form = SegundoRegistroForm()
    mis_clientes = SegundoRegistro.objects.filter(operador__username__contains=usuario)
    return render(request, 'segundo-registro.html', {'form': form, 'mis_clientes': mis_clientes})

#@login_required(login_url='/')
def SegundoRegistroEdit(request, pk, template_name='editar/segundo_registro.html'):
    clientes = get_object_or_404(SegundoRegistro, pk=pk)
    form = SegundoRegistroForm(request.POST or None, instance=clientes)
    if form.is_valid():
        form.save()
        return redirect('segundo_registro')
    return render(request, template_name, {'form': form})

#@login_required(login_url='/')
def SegundoRegistroDelete(request, pk, template_name='delete/confirmacion2.html'):
    clientes = get_object_or_404(SegundoRegistro, pk=pk)
    if request.method == 'POST':
        clientes.delete()
        return redirect('segundo_registro')
    return render(request, template_name, {'object': clientes})

#@login_required(login_url='/')
def orden_compra1(request, cliente_id=None):
    # data = serializers.serialize("json", Productos.objects.all(), fields=('pk', 'name', 'price'))
    if Order.objects.filter(Q(user__id=cliente_id) & Q(orden_compra=1)).exists():
        ordencliente = Order.objects.filter(Q(user__id=cliente_id) & Q(orden_compra=1))
        productos = ProductOrder.objects.filter(order=ordencliente)
        return render(request, 'odc/odc1-echa.html', {'ordencliente': ordencliente,
                                                      'productos': productos})
    else:
        cliente = get_object_or_404(PrimerRegistro, id=cliente_id)
        productos = Productos.objects.all()
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                user = cliente
                order_content = json.loads(request.POST['cartJSONdata'])
                order = form.save(commit=False)
                order.user = user
                order.operador = request.user
                order.total_amount = 0
                order.save()  # We have to save the order before calculate ammount
                order.total_amount = saveOrderProducts(order_content, order)
                order.save()
                books = ProductOrder.objects.filter(order=order)
                products = list(chain(books, ))
                return redirect('/clientes')
                # return render(request, 'success.html', locals())
        else:
            form = OrderForm()
        # lista = [{'pk':producto.pk, 'name':producto.nombre, 'price': Decimal(producto.precio), } for producto in productos]
        # serializado = json.dumps(lista)
        return render(request, 'odc/odc1.html', {'productos': productos,
                                                 'cliente': cliente,
                                                 'form': form,
                                                 # 'data':data,
                                                 # 'lista':serializado,
                                                 })

#@login_required(login_url='/')
def orden_compra2(request, cliente_id=None):
    if Order.objects.filter(Q(user__id=cliente_id) & Q(orden_compra=2)).exists():
        ordencliente = Order.objects.filter(Q(user__id=cliente_id) & Q(orden_compra=2))
        productos = ProductOrder.objects.filter(order=ordencliente)
        return render(request, 'odc/odc1-echa.html', {'ordencliente': ordencliente,
                                                      'productos': productos})

    else:
        cliente = get_object_or_404(PrimerRegistro, id=cliente_id)
        productos = Productos.objects.all()
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                user = cliente
                order_content = json.loads(request.POST['cartJSONdata'])
                order = form.save(commit=False)
                order.user = user
                order.operador = request.user
                order.total_amount = 0
                order.save()  # We have to save the order before calculate ammount
                order.total_amount = saveOrderProducts(order_content, order)
                order.save()
                books = ProductOrder.objects.filter(order=order)
                products = list(chain(books, ))
                return redirect('clientes')
                # return render(request, 'success.html', locals())
        else:
            form = OrderForm()
        # lista = [{'pk':producto.pk, 'name':producto.nombre, 'price': Decimal(producto.precio), } for producto in productos]
        # serializado = json.dumps(lista)
        return render(request, 'odc/odc2.html', {'productos': productos,
                                                 'cliente': cliente,
                                                 'form': form,
                                                 # 'data':data,
                                                 # 'lista':serializado,
                                                 })

#@login_required(login_url='/')
def orden_compra3(request, cliente_id=None):
    if Order.objects.filter(Q(user__id=cliente_id) & Q(orden_compra=3)).exists():
        ordencliente = Order.objects.filter(Q(user__id=cliente_id) & Q(orden_compra=2))
        productos = ProductOrder.objects.filter(order=ordencliente)
        return render(request, 'odc/odc1-echa.html', {'ordencliente': ordencliente,
                                                      'productos': productos})
    else:
        cliente = get_object_or_404(PrimerRegistro, id=cliente_id)
        productos = Productos.objects.all()
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                user = cliente
                order_content = json.loads(request.POST['cartJSONdata'])
                order = form.save(commit=False)
                order.user = user
                order.operador = request.user
                order.total_amount = 0
                order.save()  # We have to save the order before calculate ammount
                order.total_amount = saveOrderProducts(order_content, order)
                order.save()
                books = ProductOrder.objects.filter(order=order)
                products = list(chain(books, ))
                return redirect('clientes')
                # return render(request, 'success.html', locals())
        else:
            form = OrderForm()
        # lista = [{'pk':producto.pk, 'name':producto.nombre, 'price': Decimal(producto.precio), } for producto in productos]
        # serializado = json.dumps(lista)
        return render(request, 'odc/odc3.html', {'productos': productos,
                                                 'cliente': cliente,
                                                 'form': form,
                                                 # 'data':data,
                                                 # 'lista':serializado,
                                                 })
def saveOrderProducts(order_content, order):
    amount = 0
    prod_error = False
    for product in order_content:
        product_uid = product['id']
        quantity = product['quantity']
        p_price = product['price']
        amount += float(p_price) * float(quantity)
        product_obj = Productos.objects.get(pk=product_uid)
        product_obj.save()
        prod_order = order.productorder_set.create(product=product_obj, quantity=quantity)

        if not prod_error:
            prod_order.save()
    return amount

from django.db.models import Sum

def enviar_email(request, cliente_id=None):
    posta = Order.objects.filter(user=cliente_id).aggregate(Sum('total_amount'))
    post = Order.objects.filter(user=cliente_id)
    primerr = PrimerRegistro.objects.get(id = cliente_id)
    segundorr = SegundoRegistro.objects.get(cliente__id = cliente_id)
    operadort = request.user
    datos = Datos.objects.get(usuario = operadort)
    sent = False
    if request.method == 'POST':
        form = EmailOdcsForm(request.POST)
        if form.is_valid():
            enviaryael(request,cliente_id)
            cd = form.cleaned_data
            allorder = [(p.total_amount) for p in Order.objects.filter(user=cliente_id)]
            if len(allorder) == 3:
                subject = 'Mi Casita ordenes de compra + ife + caratula + tarjeta mejoravit '
                message = 'Cliente Listo \n\n\'s  datos Orden 1:{}\n\n Orden 2:{}\n\n Orden 3: {}\n\n Total:{} \n\n url archivos: {} \n\n comentario: {} '.format(allorder[0], allorder[1], allorder[2], posta['total_amount__sum'],cd['url_archivos'], cd['comments'],)
                send_mail(subject, message, 'soldiddfouns@gmail.com', [cd['to']])
                sent = True
                redirect('clientes')
            elif len(allorder) == 2:
                subject = 'Mi Casita ordenes de compra + ife + caratula + tarjeta mejoravit'
                message = 'Cliente Listo \n\n\'s  datos Orden 1:{}\n\n Orden 2:{}\n\n  Total:{} \n\n url archivos: {} \n\n comentario: {}  '.format(allorder[0], allorder[1], posta['total_amount__sum'], cd['url_archivos'], cd['comments'], )
                send_mail(subject, message, 'soldiddfouns@gmail.com', [cd['to']])
                sent = True
                redirect('clientes')
            elif len(allorder) == 1:
                subject = 'Mi Casita ordenes de compra + ife + caratula + tarjeta mejoravit'
                message = 'Cliente Listo \n\n\'s  datos Orden 1:{}\n\n Total:{} \n\n url archivos: {} \n\n comentario: {}  '.format(allorder[0], posta['total_amount__sum'], cd['url_archivos'], cd['comments'], )
                send_mail(subject, message, 'soldiddfouns@gmail.com', [cd['to']])
                sent = True
                redirect('clientes')

        else:
            return redirect('clientes')
    else:

        form = EmailOdcsForm()
        #formr =RelacionPFprm()
    return render(request, 'enviar.html', {'post': post,
                                           'posta': posta,
                                           'form': form,
                                           'sent': sent,
                                           'segundorr': segundorr,
                                           'datos':datos,
                                           #'formr':formr
                                           })

#def enviaryael(request,fecha, cliente, odc1,odc2,odc3 ,pag_clie ,p_asesor,comision,com_t,asesor,ref_pago, importe):
def enviaryael(request, cliente_id):
    contars3 =Order.objects.filter(user__id =cliente_id, orden_compra__contains =3)

    if contars3.count() > 0:
        infocliente  = PrimerRegistro.objects.get(id=cliente_id)
        asesor = infocliente.operador
        segundor = SegundoRegistro.objects.get(cliente__id=cliente_id)
        odc1 = Order.objects.get(user__id =cliente_id, orden_compra__contains =1)
        od1 = float(odc1.total_amount)
        odc2 = Order.objects.get(user__id =cliente_id, orden_compra__contains =2)
        od2 = float(odc2.total_amount)
        odc3 = Order.objects.get(user__id =cliente_id, orden_compra__contains =3)
        od3 = float(odc3.total_amount)
        totalodc = Order.objects.filter(user__id=cliente_id).aggregate(Sum('total_amount'))
        totalodcs = float(totalodc['total_amount__sum'])
        totalodcs_menos_20 = totalodcs-(totalodcs*.20)
        comision = infocliente.comision
        com = float(comision)
        p_comision = segundor.comisiona()
        pcom = float(p_comision)
        suma =  com + pcom - 100
        sumaimporte = totalodcs_menos_20 - suma
        nombre = infocliente.id
        o_cliente = PrimerRegistro.objects.get(id=nombre)
        fecha = timezone.now()
        form = RelacionP.objects.create(
                    fecha = fecha,
                    cliente =  o_cliente,
                    odc1 = od1,
                    odc2 = od2,
                    odc3 = od3,
                    pag_clie = totalodcs_menos_20,
                    p_asesor = pcom ,
                    comision = com,
                    com_t = suma,
                    asesor = asesor,
                    # ref_pago = request.POST['ref_pago'],
                    importe = sumaimporte,
                )
    contars2 =Order.objects.filter(user__id =cliente_id, orden_compra__contains =2)
    if contars2.count() > 0:
        infocliente  = PrimerRegistro.objects.get(id=cliente_id)
        asesor = infocliente.operador
        segundor = SegundoRegistro.objects.get(cliente__id=cliente_id)
        odc1 = Order.objects.get(user__id =cliente_id, orden_compra__contains =1)
        od1 = float(odc1.total_amount)
        odc2 = Order.objects.get(user__id =cliente_id, orden_compra__contains =2)
        od2 = float(odc2.total_amount)
        totalodc = Order.objects.filter(user__id=cliente_id).aggregate(Sum('total_amount'))
        totalodcs = float(totalodc['total_amount__sum'])
        totalodcs_menos_20 = totalodcs-(totalodcs*.20)
        comision = infocliente.comision
        com = float(comision)
        p_comision = segundor.comisiona()
        pcom = float(p_comision)
        suma =  com + pcom -100
        sumaimporte = totalodcs_menos_20 - suma
        nombre = infocliente.id
        o_cliente = PrimerRegistro.objects.get(id=nombre)
        fecha = timezone.now()
        form = RelacionP.objects.create(
                    fecha = fecha,
                    cliente =  o_cliente,
                    odc1 = od1,
                    odc2 = od2,
                    #odc3 = od3,
                    pag_clie = totalodcs_menos_20,
                    p_asesor = pcom ,
                    comision = com,
                    com_t = suma,
                    asesor = asesor,
                    # ref_pago = request.POST['ref_pago'],
                    importe = sumaimporte,
                )
    else:
        infocliente  = PrimerRegistro.objects.get(id=cliente_id)
        asesor = infocliente.operador
        segundor = SegundoRegistro.objects.get(cliente__id=cliente_id)
        odc1 = Order.objects.get(user__id =cliente_id, orden_compra__contains =1)
        od1 = float(odc1.total_amount)
        totalodc = Order.objects.filter(user__id=cliente_id).aggregate(Sum('total_amount'))
        totalodcs = float(totalodc['total_amount__sum'])
        totalodcs_menos_20 = totalodcs-(totalodcs*.20)
        comision = infocliente.comision
        com = float(comision)
        p_comision = segundor.comisiona()
        pcom = float(p_comision)
        suma =  com + pcom - 100
        sumaimporte = totalodcs_menos_20 - suma
        nombre = infocliente.id
        o_cliente = PrimerRegistro.objects.get(id=nombre)
        fecha = timezone.now()
        form = RelacionP.objects.create(
                    fecha = fecha,
                    cliente =  o_cliente,
                    odc1 = od1,
                    #odc2 = od2,
                    pag_clie = totalodcs,
                    p_asesor = pcom ,
                    comision = com,
                    com_t = suma,
                    asesor = asesor,
                    # ref_pago = request.POST['ref_pago'],
                    importe = sumaimporte,
                )
        return redirect('clientes')

def dia(request, year, month,):
    hoy = datetime.date.today()
    diass =  get_list_or_404(RelacionP, fecha__year=year,
                                        fecha__month=month,)
    mes = month
    anio = year

    rform = BuscarDiaForm()
    refrencia_form = PReferenciaForm()
    boleanRefePagform = PRBoleanPagoForm()
    odcsPagadas = OdcsPagadasForm()
    mes_actual = hoy.month
    return render(request, 'gaeladmin/dia.html', {
                                                    'form':rform,
                                                    'r_form':refrencia_form,
                                                    'b_rform':boleanRefePagform,
                                                    'odcs_p':odcsPagadas,
                                                    'mes_actual':mes_actual,
                                                    #'form': form,
                                                   'diass':diass,
                                                   'mes':mes,
                                                   'anio':anio,
                                                  })
def calendario(request):
    hoy = datetime.date.today()
    diass = RelacionP.objects.filter(fecha__year=hoy.year,
                                     fecha__month=hoy.month)
    if request.method == 'POST':
        if 'fecha_calendario' in request.POST:
            form = BuscarDiaForm(request.POST)
            if form.is_valid():
                 fetch = form.cleaned_data['fecha']
                 year = fetch.year
                 month = fetch.month
                 return dia(request, year, month)
        elif 'referencia_pago' in request.POST:
            forma = PReferenciaForm(request.POST)
            if forma.is_valid():
                client = forma.cleaned_data['cliente']
                cliente = RelacionP.objects.get(cliente__id =client)
                cliente.ref_pago = forma.cleaned_data['ref_pago']
                #cliente.crbd_rpago = forma.cleaned_data['crbd_rpago']
                cliente.save(update_fields=['ref_pago'])
                return redirect('calendario')
        elif 'cheque_cobrado' in request.POST:
            forma = PRBoleanPagoForm(request.POST)
            if forma.is_valid():
                client = forma.cleaned_data['clienteb']
                cliente = RelacionP.objects.get(cliente__id =client)
                cliente.crbd_rpago = forma.cleaned_data['crbd_rpago']
                #cliente.crbd_rpago = forma.cleaned_data['crbd_rpago']
                cliente.save(update_fields=['crbd_rpago'])
                return redirect('calendario')
        elif 'ordenes_pagadas' in request.POST:
            forma = OdcsPagadasForm(request.POST)
            if forma.is_valid():
                client = forma.cleaned_data['clientec']
                cliente = RelacionP.objects.get(cliente__id =client)
                #if forma.cleaned_data['odc1p'] == True and forma.cleaned_data['odc2p'] ==None and forma.cleaned_data['odc3p'] == None:
                cliente.odc1p = forma.cleaned_data['odc1p']
                cliente.odc2p = forma.cleaned_data['odc2p']
                cliente.odc3p = forma.cleaned_data['odc3p']
                cliente.save(update_fields=['odc1p', 'odc2p', 'odc3p'])
                return redirect('calendario')
                #elif forma.cleaned_data['odc1p'] == True and forma.cleaned_data['odc2p'] == True and forma.cleaned_data['odc3p'] == True:

    rform = BuscarDiaForm()
    refrencia_form = PReferenciaForm()
    boleanRefePagform = PRBoleanPagoForm()
    odcsPagadas = OdcsPagadasForm()
    mes_actual = hoy.month
    return render(request, 'gaeladmin/calendar.html', {
                                                        'form':rform,
                                                        'diass':diass,
                                                        'r_form':refrencia_form,
                                                        'b_rform':boleanRefePagform,
                                                        'odcs_p':odcsPagadas,
                                                        'mes_actual':mes_actual,})
def cargar_pdfs(request, id):
    form = CargarPdfsForm
    return render(request, 'cargar-pdf/cargar-pdfs.html', {'form':form})

def cliente_perfil(request, id):
    obtenerClientePR = PrimerRegistro.objects.get(id=id)
    obtenerTgts = SegundoRegistro.objects.get(cliente__id = id)
    return render(request, 'perfil/peril-cliente.html', {'primer':obtenerClientePR,
                                                         'segundo': obtenerTgts})

def sucursales(request):
    datosusuarios = Datos.objects.all()
    sucursales = Sucursal.objects.all()
    return render(request, 'gaeladmin/sucursales/sucursales.html', {
                                                        'datos':datosusuarios,
                                                        'sucursales': sucursales,
    })
#sucursal personalizada
def sucursal_unica(request, pk):
    sucsl = Sucursal.objects.get(id = pk)
    suc = sucsl.id
    gs = GatosSucursal.objects.filter(sucursal__id = suc)
    datos = Datos.objects.filter(sucursal__id = suc)
    return render(request, 'gaeladmin/sucursales/sucursal-unica.html', {'sucsl': sucsl,
                                                                        'gs': gs,
                                                                        'datos':datos,})
def gastos_oficina(request):
    usuario = request.user
    datos = Datos.objects.get(usuario=usuario)
    sucursal = datos.sucursal.id

    if request.method == 'POST':
        form = GatosSucursalForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.sucursal =sucursal
            gasto.save()
            return redirect('gastos_oficina')
    datosusuarios = Datos.objects.filter(sucursal=sucursal)
    datossucursales = Sucursal.objects.filter(id=sucursal)
    form = GatosSucursalForm()
    gs = GatosSucursal.objects.filter(sucursal=sucursal)
    return  render(request,'asistente/gastos-oficina.html', {'datos':datos,
                                                             'form':form,
                                                             'gs':gs,
                                                             'datosusuarios':datosusuarios,
                                                             'datossucursal':datossucursales})
def empleado_perfil(request, id):
    obtenerEmpleado = Datos.objects.get(id=id)
    return render(request, 'perfil/perfil-empleado.html',{'primer':obtenerEmpleado,})

def comisiones_admingael(request):
    if request.method == 'POST':
        if 'fecha_calendario' in request.POST:
            form = BuscarDiaForm(request.POST)
            if form.is_valid():
                 fetch = form.cleaned_data['fecha']
                 year = fetch.year
                 month = fetch.month
                 return dia(request, year, month)
    rp_comisiones = RelacionP.objects.all()
    rform = BuscarDiaForm()
    hoy = datetime.date.today()
    mes_actual = hoy.month
    return render(request, 'gaeladmin/comisiones-gael.html',{
                                            'mes_actual': mes_actual,
                                            'rp_comisiones':rp_comisiones,
                                            'form':rform,})

def ver_resumencom(request,year, month, day):
    sacar_asesor_db=get_list_or_404(RelacionP, fecha__year=2016,
                                        fecha__month=2,
                                        fecha__day=23,)

    sacar_asesor = RelacionP.objects.filter(fecha__year=2016,
                                        fecha__month=2,
                                        fecha__day=23,)
    asesoress = []
    for asesor in sacar_asesor:
        asesoress.append((asesor.asesor))

    asesoressd = []
    for asesord in sacar_asesor:
        asesoressd.append({
                    'asesor': asesord.asesor,
                    'total': RelacionP.objects.filter(Q(asesor__username =asesord.asesor) & Q(fecha__year=2016,
                                        fecha__month=2,
                                        fecha__day=23,)).aggregate(Sum('com_t')),
                         })

    sumar_tot_ase = RelacionP.objects.filter(Q(asesor__username__in =asesoress) & Q(fecha__year=2016,
                                        fecha__month=2,
                                        fecha__day=23,)).aggregate(Sum('com_t'))
    sumar_tot_ase1 = RelacionP.objects.filter(Q(asesor__username__in =asesoress) & Q(fecha__year=2016,
                                        fecha__month=2,
                                        fecha__day=23,))

    return render(request, 'gaeladmin/resumen_dia_comision.html', {'diass': sacar_asesor,
                                                                   'sumar_tot_ase':sumar_tot_ase,
                                                                   'sumar_tot_ase1':sumar_tot_ase1,
                                                                    'asesoressd':asesoressd  ,
                                                                   })
