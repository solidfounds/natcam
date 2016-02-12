from itertools import chain
from django.core.mail import send_mail
from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from .forms import PrimerRegistroFORM, SegundoRegistroForm, OrderForm, EmailOdcsForm, CargarPdfsForm
from django.http import HttpResponseRedirect
from .models import PrimerRegistro, SegundoRegistro, Productos, ProductOrder, Order, RelacionP
#from users.models import User
from django.contrib.auth.decorators import login_required
from  django.core import serializers
import json
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User

def index(request):
    return render(request, 'index.html', )


def nota_remision(request):
    return render(request, 'nota-remision.html')

#@login_required(login_url='/')
def clientes(request):
    usuario = request.user
    cliente = PrimerRegistro.objects.filter(operador__username__contains=usuario)
    tarjeta = SegundoRegistro.objects.filter(operador__username__contains=usuario)
    ordenes = Order.objects.filter(operador__username__contains=usuario)
    orden1 = Order.objects.filter(Q(orden_compra="1") & Q(operador__username__contains=usuario))
    orden2 = Order.objects.filter(Q(orden_compra="2") & Q(operador__username__contains=usuario))
    orden3 = Order.objects.filter(Q(orden_compra="3") & Q(operador__username__contains=usuario))
    # odcf  = ['1', '2', '3']
    # q_objects = Q()

    odcs = Order.objects.filter(Q(operador__username__contains=usuario))
    return render(request, 'clientes.html', {
        'cliente': cliente,
        'tarjeta': tarjeta,
        'ordenes': ordenes,
        'orden1': orden1,
        'orden2': orden2,
        'orden3': orden3,
        'odcs': odcs,
    })


#@login_required(login_url='/')
def desempeno(request):
    usuario = request.user
    mi_info = User.objects.get(username=usuario)
    total_clientes = PrimerRegistro.objects.filter(operador__username__contains=usuario).count()
    micomision = PrimerRegistro.objects.filter(operador__username__contains=usuario)
    micomiscionAsesor = SegundoRegistro.objects.filter(operador__username__contains=usuario)
    #percepcion = SegundoRegistro.objects.filter(operador__username__contains=usuario).aggregate(Sum('micomision'))
    return render(request, 'desempeno.html', {'mi_info': mi_info,
                                              'total_clientes': total_clientes,
                                              'micomision':micomision,
                                              'micomiscionAsesor':micomiscionAsesor,
                                              #'percepcion': percepcion
                                              })


#@login_required(login_url='/')
def primerRegistro(request):
    usuario = request.user
    if request.method == 'POST':
        form = PrimerRegistroFORM(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.operador = usuario
            post.save()
            return redirect('agregar_clientes')
    else:
        form = PrimerRegistroFORM()
    mis_clientes = PrimerRegistro.objects.filter(operador__username__contains=usuario)
    return render(request, 'index.html', {'form': form, 'mis_clientes': mis_clientes})


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
    ife = primerr.ife
    sent = False
    if request.method == 'POST':
        form = EmailOdcsForm(request.POST)
        if form.is_valid():
            enviaryael(request,cliente_id)
            cd = form.cleaned_data
            # post_url = request.build_absolute_uri(post.get_absolute_url())
            # fetch = [(f.order_date) for f in Order.objects.filter(user = cliente_id)]
            allorder = [(p.total_amount) for p in Order.objects.filter(user=cliente_id)]
            subject = '  recommends you reading '
            message = 'Cliente Listo \n\n\'s  datos Orden 1:{}\n\n Orden 2:{}\n\n Orden 3: {}\n\n Total:{}  comments: {} '.format(allorder[0], allorder[1], allorder[2], posta['total_amount__sum'], cd['comments'], )
            message.attach('ife')
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
                                           #'formr':formr
                                           })

#def enviaryael(request,fecha, cliente, odc1,odc2,odc3 ,pag_clie ,p_asesor,comision,com_t,asesor,ref_pago, importe):
def enviaryael(request, cliente_id):
    infocliente  = PrimerRegistro.objects.get(id=cliente_id)
    segundor = SegundoRegistro.objects.get(id=cliente_id)
    odc1 = Order.objects.get(user__id =cliente_id, orden_compra__contains =1)
    od1 = float(odc1.total_amount)
    odc2 = Order.objects.get(user__id =cliente_id, orden_compra__contains =2)
    od2 = float(odc2.total_amount)
    odc3 = Order.objects.get(user__id =cliente_id, orden_compra__contains =3)
    od3 = float(odc3.total_amount)
    totalodc = Order.objects.filter(user__id=cliente_id).aggregate(Sum('total_amount'))
    totalodcs = float(totalodc['total_amount__sum'])
    # for odcss in odcs:
    #     odcss.orden_compra
    #odcs1 = odcs.orden_compra
    comision = infocliente.comision
    com = float(comision)
    p_comision = segundor.comisiona()
    pcom = float(p_comision)
    suma = com + pcom
    sumaimporte = totalodcs -suma
    #ordenes = Order.objects.filter(cliente=cliente_id)
    nombre = infocliente.id
    fecha = timezone.now()
    form = RelacionP.objects.create(
                fecha = fecha,
                #cliente =  nombre,
                odc1 = od1,
                odc2 = od2,
                odc3 = od3,
                pag_clie = totalodcs,
                p_asesor = pcom ,
                comision = com,
                com_t = suma,
                asesor = request.user,
                # ref_pago = request.POST['ref_pago'],
                importe = sumaimporte,
            )
    return redirect('clientes')

def dia(request, year, month, day):
    #form = RelacionPFprm()
    diass =  get_list_or_404(RelacionP, fecha__year=year,
                                        fecha__month=month,
                                        fecha__day=day,)
    return render(request, 'gaeladmin/dia.html', {
                                                    #'form': form,
                                                   'diass':diass
                                                  })


from calendar import HTMLCalendar
from datetime import date
from  itertools import groupby
from  django.utils.html import conditional_escape as esc
from .forms import BuscarDiaForm
def calendario(request):
    if request.method == 'POST':
        cs = BuscarDiaForm(request.POST)
        if cs.is_valid():
             datos = cs.fecha.split("-")
             year = datos[0]
             month = datos[1]
             day = datos[2]
             return dia(request, year, month, day)
    else:
        form = BuscarDiaForm()
    return render(request, 'gaeladmin/calendar.html', {'form':form})

def cargar_pdfs(request, id):
    form = CargarPdfsForm
    return render(request, 'cargar-pdf/cargar-pdfs.html', {'form':form})


