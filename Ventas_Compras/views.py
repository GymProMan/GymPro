from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from Ventas_Compras.forms import ProductForm, ProveedorForm, BuscarProductoForm, RegistrarCompraForm
from Ventas_Compras.models import Producto, Proveedor, Compras_Producto, Compras, Ventas_Producto, Ventas, \
    Ventas_Membresias


# Create your views here.
@login_required
def index_ventas(request):
    return render(request, 'index_ventas.html')


@login_required
def crear_productos(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductForm()

    return render(request, 'crear_producto.html', {'form': form})


@login_required
def listar_productos(request):
    # Filtra los productos con estado = 1
    productos = Producto.objects.filter(estado=1)
    return render(request, 'listar_productos.html', {"productos": productos})


@login_required
def editar_productos(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductForm(instance=producto)

    return render(request, 'editar_producto.html', {'form': form})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@login_required
@csrf_exempt
def eliminar_productos(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        if producto.existencias < 1:
            producto.estado = 0
            producto.save()  # Guarda el cambio de estado
            return JsonResponse({'success': True, 'mensaje': 'Producto eliminado con éxito.'})
        else:
            return JsonResponse(
                {'success': False, 'mensaje': 'No se puede eliminar un producto que cuente con existencias.'},
                status=400)

    return JsonResponse({'success': False, 'mensaje': 'Método no permitido.'}, status=405)


@login_required
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm()

    return render(request, 'crear_proveedor.html', {'form': form})


@login_required
def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)

    return render(request, 'editar_proveedor.html', {'form': form})


@login_required
def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'listar_proveedores.html', {"proveedores": proveedores})


@login_required
def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('listar_proveedores')

    return render(request, 'eliminar_proveedor.html', {'proveedor': proveedor})


@login_required
def registrar_compra(request):
    productos_comprados = request.session.get('productos_comprados', [])
    total_compra = sum([p['precio_total'] for p in productos_comprados])
    mensaje_error = None

    if 'buscar_producto' in request.POST:
        buscar_form = BuscarProductoForm(request.POST)
        if buscar_form.is_valid():
            codigo_producto = buscar_form.cleaned_data['codigo_producto']
            cantidad = buscar_form.cleaned_data['cantidad']
            try:
                producto = Producto.objects.get(codigo=codigo_producto)
                producto_en_lista = next((p for p in productos_comprados if p['codigo'] == codigo_producto), None)
                if producto_en_lista:
                    producto_en_lista['cantidad'] += cantidad
                    producto_en_lista['precio_total'] = producto_en_lista['cantidad'] * producto.precio
                else:
                    producto_info = {
                        'nombre': producto.nombre,
                        'precio_unitario': producto.precio,
                        'cantidad': cantidad,
                        'precio_total': cantidad * producto.precio,
                        'codigo': producto.codigo
                    }
                    productos_comprados.append(producto_info)
                total_compra = sum([p['precio_total'] for p in productos_comprados])
                request.session['productos_comprados'] = productos_comprados  # Guardar en la sesión
            except Producto.DoesNotExist:
                mensaje_error = 'El producto no existe'
    else:
        buscar_form = BuscarProductoForm()

    if 'registrar_compra' in request.POST:
        compra_form = RegistrarCompraForm(request.POST)
        if compra_form.is_valid() and productos_comprados:
            compra = compra_form.save(commit=False)
            compra.total = total_compra
            compra.usuario = request.user
            compra.save()

            for p in productos_comprados:
                producto = Producto.objects.get(codigo=p['codigo'])
                producto.existencias += p['cantidad']
                producto.save()
                Compras_Producto.objects.create(
                    compra=compra,
                    producto=producto,
                    cantidad_productos=p['cantidad']
                )

            request.session.pop('productos_comprados', None)

            return HttpResponseRedirect(reverse('listar_compras'))

    else:
        compra_form = RegistrarCompraForm()

    return render(request, 'registrar_compra.html', {
        'buscar_form': buscar_form,
        'compra_form': compra_form,
        'productos_comprados': productos_comprados,
        'total_compra': total_compra,
        'mensaje_error': mensaje_error,
    })


@login_required
def registrar_venta(request):
    productos_vendidos = request.session.get('productos_vendidos', [])
    total_venta = sum([p['precio_total'] for p in productos_vendidos])
    mensaje_error = None

    if 'buscar_producto' in request.POST:
        buscar_form = BuscarProductoForm(request.POST)
        if buscar_form.is_valid():
            codigo_producto = buscar_form.cleaned_data['codigo_producto']
            cantidad = buscar_form.cleaned_data['cantidad']
            try:
                producto = Producto.objects.get(codigo=codigo_producto)
                if producto.existencias >= cantidad:
                    producto_en_lista = next((p for p in productos_vendidos if p['codigo'] == codigo_producto), None)
                    if producto_en_lista:
                        producto_en_lista['cantidad'] += cantidad
                        producto_en_lista['precio_total'] = producto_en_lista['cantidad'] * producto.precio
                    else:
                        producto_info = {
                            'nombre': producto.nombre,
                            'precio_unitario': producto.precio,
                            'cantidad': cantidad,
                            'precio_total': cantidad * producto.precio,
                            'codigo': producto.codigo
                        }
                        productos_vendidos.append(producto_info)
                    total_venta = sum([p['precio_total'] for p in productos_vendidos])
                    request.session['productos_vendidos'] = productos_vendidos  # Guardar en la sesión
                else:
                    mensaje_error = 'No hay suficientes existencias del producto'
            except Producto.DoesNotExist:
                mensaje_error = 'El producto no existe'
    else:
        buscar_form = BuscarProductoForm()

    if 'registrar_venta' in request.POST:
        if productos_vendidos:
            venta = Ventas.objects.create(
                total=total_venta,
                usuario=request.user,
                pom="Producto"
            )

            for p in productos_vendidos:
                producto = Producto.objects.get(codigo=p['codigo'])

                if producto.existencias >= p['cantidad']:
                    producto.existencias -= p['cantidad']
                    producto.save()

                    Ventas_Producto.objects.create(
                        venta=venta,
                        producto=producto,
                        cantidad_productos=p['cantidad']
                    )
                else:
                    mensaje_error = f'No hay existencias suficientes para el producto {producto.nombre}'
                    break

            request.session.pop('productos_vendidos', None)

            return HttpResponseRedirect(reverse('listar_ventas'))

    return render(request, 'registrar_venta.html', {
        'buscar_form': buscar_form,
        'productos_vendidos': productos_vendidos,
        'total_venta': total_venta,
        'mensaje_error': mensaje_error,
    })


def listar_compras(request):
    compras = Compras.objects.all().order_by('-fecha_compra')  # Ordenadas por fecha más reciente
    return render(request, 'listar_compras.html', {'compras': compras})

def listar_ventas(request):
    ventas = Ventas.objects.all().order_by('-fecha_venta')  # Ordenadas por fecha más reciente
    return render(request, 'listar_ventas.html', {'ventas': ventas})




def detalle_compra(request, compra_id):
    compra = get_object_or_404(Compras, id=compra_id)
    productos = Compras_Producto.objects.filter(compra=compra)

    productos_detalle = []
    for item in productos:
        total_precio = item.cantidad_productos * item.producto.precio
        productos_detalle.append({
            'producto': item.producto,
            'cantidad': item.cantidad_productos,
            'precio_unitario': item.producto.precio,
            'precio_total': total_precio,
        })

    return render(request, 'detalle_compra.html', {'compra': compra, 'productos': productos_detalle})


def detalle_venta(request, venta_id, tipo):
    venta = get_object_or_404(Ventas, id=venta_id)
    if tipo=="Producto":
        productos = Ventas_Producto.objects.filter(venta=venta)
        productos_detalle = []
        for item in productos:
            total_precio = item.cantidad_productos * item.producto.precio
            productos_detalle.append({
                'producto': item.producto,
                'cantidad': item.cantidad_productos,
                'precio_unitario': item.producto.precio,
                'precio_total': total_precio,
            })
            return render(request, 'detalle_venta.html', {'venta': venta, 'productos': productos_detalle})
    else:
        membresias = Ventas_Membresias.objects.filter(venta=venta)
        membresia_detalle = []
        for item in membresias:
            membresia_detalle.append({
                'membresia': item.membresia,
                'cantidad': "1",
                'precio_total': item.membresia.costo,
            })
        return render(request, 'detalle_venta_memebresia.html', {'venta': venta, 'membresias': membresia_detalle})






#Graficas de ingresos_totales_por_mes
from django.db.models import Sum
from django.db.models.functions import ExtractYear, ExtractMonth
def ingresos_totales_por_mes(request):
    # Agrupar las ventas por año y mes, y sumar los totales
    ingresos = (
        Ventas.objects.annotate(anio=ExtractYear('fecha_venta'), mes=ExtractMonth('fecha_venta'))
        .values('anio', 'mes')
        .annotate(total_ingresos=Sum('total'))
        .order_by('anio', 'mes')
    )
    # Preparar datos para el frontend
    labels = [f"{item['anio']}-{item['mes']:02d}" for item in ingresos]  # Formato: Año-Mes
    data = [float(item['total_ingresos']) for item in ingresos]
    return JsonResponse({'labels': labels, 'data': data})



def stock_productos(request):
    # Obtener los productos y sus existencias
    productos = Producto.objects.filter(estado=1).values('nombre', 'existencias')
    labels = [producto['nombre'] for producto in productos]
    data = [producto['existencias'] for producto in productos]
    return JsonResponse({'labels': labels, 'data': data})