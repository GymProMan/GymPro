from datetime import timedelta, date

import pytz
from cloudinary.uploader import upload
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.utils import timezone
from django.contrib import messages

from GYM_PRO import settings
from Ventas_Compras.models import Ventas, Ventas_Membresias
from .forms import MiembroForm, MembresiaForm, MembresiaTipoForm, ClaveAccesoForm, FiltroAsistenciaForm
from .models import Membresia, MembresiaTipo, Miembro, Asistencia


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
@transaction.atomic
def crear_miembro_membresia(request):
    if request.method == 'POST':
        miembro_form = MiembroForm(request.POST, request.FILES)
        membresia_form = MembresiaForm(request.POST)

        if miembro_form.is_valid() and membresia_form.is_valid():
            miembro = miembro_form.save(commit=False)  # Guardar parcialmente para modificar antes de la inserción

            # Generar clave para el miembro
            ultimo_miembro = Miembro.objects.order_by('-clave').first()
            if ultimo_miembro and ultimo_miembro.clave.isdigit():
                miembro.clave = str(int(ultimo_miembro.clave) + 1)
            else:
                miembro.clave = "1"

            # Subir la foto a Cloudinary si está presente
            if 'foto' in request.FILES:
                try:
                    result = upload(
                        request.FILES['foto'],
                        cloud_name=settings.CLOUDINARY_STORAGE.get('CLOUDINARY_CLOUD_NAME'),
                        api_key=settings.CLOUDINARY_STORAGE.get('CLOUDINARY_API_KEY'),
                        api_secret=settings.CLOUDINARY_STORAGE.get('CLOUDINARY_API_SECRET')
                    )
                    miembro.foto_cloud = result['secure_url']  # Asignar la URL de la foto en Cloudinary
                except Exception as e:
                    print(f"Error al subir la imagen: {e}")
                    return render(request, 'miembro_membresia_form.html', {
                        'miembro_form': miembro_form,
                        'membresia_form': membresia_form,
                        'error': 'Hubo un error al subir la imagen. Por favor, inténtalo nuevamente.'
                    })

            miembro.save()  # Guardar el modelo con todos los datos completos

            # Manejar la membresía
            membresia = membresia_form.save(commit=False)
            membresia.miembro = miembro
            tipo_membresia = membresia.tipo_membresia
            fecha_inicio = membresia.fecha_inicio

            if tipo_membresia.unidad_tiempo == 'Dias':
                membresia.fecha_final = fecha_inicio + timedelta(days=tipo_membresia.duracion)
            elif tipo_membresia.unidad_tiempo == 'Semanas':
                membresia.fecha_final = fecha_inicio + timedelta(weeks=tipo_membresia.duracion)
            elif tipo_membresia.unidad_tiempo == 'Meses':
                membresia.fecha_final = fecha_inicio + timedelta(days=30 * tipo_membresia.duracion)
            elif tipo_membresia.unidad_tiempo == 'Años':
                membresia.fecha_final = fecha_inicio + timedelta(days=365 * tipo_membresia.duracion)

            membresia.save()

            # Registrar la venta
            venta = Ventas.objects.create(
                usuario=request.user,
                fecha_venta=membresia.fecha_inicio,
                total=tipo_membresia.costo,
                pom="Membresia"
            )
            if venta:
                Ventas_Membresias.objects.create(
                    membresia=tipo_membresia,
                    venta=venta,
                )

            # Agregar clave al contexto para el SweetAlert
            return render(request, 'miembro_membresia_form.html', {
                'miembro_form': MiembroForm(),
                'membresia_form': MembresiaForm(),
                'success': True,
                'clave': miembro.clave,  # Pasar la clave generada
            })

        return render(request, 'miembro_membresia_form.html', {
            'miembro_form': miembro_form,
            'membresia_form': membresia_form,
        })
    else:
        miembro_form = MiembroForm()
        membresia_form = MembresiaForm()
    return render(request, 'miembro_membresia_form.html', {
        'miembro_form': miembro_form,
        'membresia_form': membresia_form,
    })


from datetime import date


@login_required
def miembros_lista(request):
    miembros = Miembro.objects.all()
    membresias_activa = Membresia.objects.filter(fecha_final__gte=date.today())
    fecha_actual = timezone.now().astimezone(pytz.timezone('America/Mexico_City'))

    return render(request, 'miembro_lista.html',
                  {'miembros': miembros, 'fecha_actual': fecha_actual, 'membresias_activa': membresias_activa})


@login_required
def registrar_asistencia(request):
    mensaje = None
    error = None

    if request.method == "POST":
        if request.headers.get("Content-Type") == "application/json":
            import json
            data = json.loads(request.body)
            clave_ingresada = data.get("clave")
        else:
            form = ClaveAccesoForm(request.POST)
            if form.is_valid():
                clave_ingresada = form.cleaned_data["clave"]
            else:
                clave_ingresada = None

        if clave_ingresada:
            try:
                miembro = Miembro.objects.get(clave=clave_ingresada)

                membresia_activa = Membresia.objects.filter(
                    miembro=miembro, fecha_final__gte=date.today()
                ).exists()

                if membresia_activa:
                    fecha_actual = timezone.now().astimezone(pytz.timezone('America/Mexico_City')).date()
                    hora_actual = timezone.now().astimezone(pytz.timezone('America/Mexico_City')).time()
                    Asistencia.objects.create(miembro=miembro, fecha=fecha_actual, hora=hora_actual)
                    mensaje = f"Acceso concedido. Asistencia registrada para {miembro.nombre}."

                else:
                    error = f"Acceso denegado. Membresía inactiva, adquiera una nueva membresía."
            except Miembro.DoesNotExist:
                error = "Clave inválida. No se encontró ningún miembro con esa clave."
        else:
            error = "No se proporcionó una clave válida."

        if request.headers.get("Content-Type") == "application/json":
            return JsonResponse({"success": not error, "mensaje": mensaje or error})

    else:
        form = ClaveAccesoForm()

    return render(request, "registrar_asistencia.html", {"form": form, "mensaje": mensaje, "error": error})


@login_required
def listar_asistencias(request):
    asistencias = Asistencia.objects.all()
    form = FiltroAsistenciaForm(request.GET or None)

    if form.is_valid():
        if form.cleaned_data['fecha']:
            asistencias = asistencias.filter(fecha=form.cleaned_data['fecha'])
        if form.cleaned_data['miembro']:
            asistencias = asistencias.filter(miembro=form.cleaned_data['miembro'])

    return render(request, 'listar_asistencias.html', {'form': form, 'asistencias': asistencias})


@login_required
def actualizar_miembro(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    if request.method == 'POST':
        miembro_form = MiembroForm(request.POST, request.FILES, instance=miembro)
        if miembro_form.is_valid():
            # Subir nueva foto a Cloudinary si se proporciona
            if 'foto' in request.FILES:
                try:
                    result = upload(
                        request.FILES['foto'],
                        cloud_name=settings.CLOUDINARY_STORAGE.get('CLOUDINARY_CLOUD_NAME'),
                        api_key=settings.CLOUDINARY_STORAGE.get('CLOUDINARY_API_KEY'),
                        api_secret=settings.CLOUDINARY_STORAGE.get('CLOUDINARY_API_SECRET')
                    )
                    miembro.foto_cloud = result['secure_url']  # Actualizar la URL de la foto en Cloudinary
                except Exception as e:
                    print(f"Error al subir la imagen: {e}")
                    return render(request, 'actualizar_miembro.html', {
                        'miembro_form': miembro_form,
                        'miembro': miembro,
                        'error': 'Hubo un error al subir la imagen. Por favor, inténtalo nuevamente.'
                    })

            miembro_form.save()  # Guardar los cambios en la base de datos
            # Indicar éxito en la actualización
            return render(request, 'actualizar_miembro.html', {
                'miembro_form': miembro_form,
                'miembro': miembro,
                'success': True
            })
    else:
        miembro_form = MiembroForm(instance=miembro)

    return render(request, 'actualizar_miembro.html', {
        'miembro_form': miembro_form,
        'miembro': miembro
    })



from django.http import JsonResponse
from django.shortcuts import redirect


@login_required
def asignar_membresia(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    membresia_activa = Membresia.objects.filter(miembro=miembro, fecha_final__gte=date.today()).exists()

    # Si tiene membresía activa y es una solicitud AJAX, devuelve un error en JSON
    if membresia_activa:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Este miembro ya tiene una membresía activa.'}, status=400)

        # Si no es AJAX, redirige a una página de error o muestra el mensaje.
        return render(request, 'error.html', {'mensaje': 'Este miembro ya tiene una membresía activa.'})

    # Si no tiene membresía activa, muestra el formulario o guarda los datos.
    if request.method == 'POST':
        membresia_form = MembresiaForm(request.POST)
        if membresia_form.is_valid():
            membresia = membresia_form.save(commit=False)
            membresia.miembro = miembro
            membresia.save()

            # Crear venta y vincular membresía
            venta = Ventas.objects.create(
                usuario=request.user,
                fecha_venta=membresia.fecha_inicio,
                total=membresia.tipo_membresia.costo,
                pom="Membresia"
            )
            if venta:
                Ventas_Membresias.objects.create(
                    membresia=membresia.tipo_membresia,
                    venta=venta,
                )

            return redirect('miembros_lista')
    else:
        membresia_form = MembresiaForm()

    return render(request, 'asignar_membresia.html', {'membresia_form': membresia_form, 'miembro': miembro})


@login_required
def crear_tipo_membresia(request):
    if request.method == 'POST':
        form = MembresiaTipoForm(request.POST)
        if form.is_valid():
            form.save()
            # Indicar que el guardado fue exitoso
            return render(request, 'crear_tipo_membresia.html', {'form': form, 'success': True})
    else:
        form = MembresiaTipoForm()

    return render(request, 'crear_tipo_membresia.html', {'form': form})


@login_required
def lista_tipos_membresia(request):
    tipos_membresia = MembresiaTipo.objects.filter(activo=True)
    return render(request, 'lista_tipos_membresia.html', {'tipos_membresia': tipos_membresia})


login_required


def actualizar_tipo_membresia(request, pk):
    tipo_membresia = get_object_or_404(MembresiaTipo, pk=pk)
    if request.method == 'POST':
        form = MembresiaTipoForm(request.POST, instance=tipo_membresia)
        if form.is_valid():
            form.save()
            # Enviamos una variable al template para indicar que se ha actualizado correctamente
            return render(request, 'actualizar_tipo_membresia.html', {
                'form': form,
                'tipo_membresia': tipo_membresia,
                'success': True
            })
    else:
        form = MembresiaTipoForm(instance=tipo_membresia)

    return render(request, 'actualizar_tipo_membresia.html', {'form': form, 'tipo_membresia': tipo_membresia})


from django.http import JsonResponse


@login_required
def eliminar_tipo_membresia(request, pk):
    if request.method == 'POST':
        tipo_membresia = get_object_or_404(MembresiaTipo, pk=pk)
        membresias = Membresia.objects.filter(tipo_membresia=tipo_membresia)

        for membresia in membresias:
            if membresia.fecha_final >= date.today():
                return JsonResponse(
                    {'mensaje': 'No se puede eliminar un tipo de membresía que cuenta con usuarios activos.'},
                    status=400)

        tipo_membresia.activo = False
        tipo_membresia.save()
        return JsonResponse({'mensaje': 'El tipo de membresía se eliminó con éxito.'})

    return JsonResponse({'mensaje': 'Método no permitido.'}, status=405)


def convertir_a_zona_horaria_mexico(fecha_hora):
    zona_horaria_mexico = pytz.timezone('America/Mexico_City')
    return fecha_hora.astimezone(zona_horaria_mexico)


def dashboard_data(request):
    ingresos_mensuales = 0.0
    membresias_activasl = Membresia.objects.filter(fecha_final__gte=date.today())
    membresias_activas = membresias_activasl.count()
    ventas_mes = Ventas.objects.filter(fecha_venta__month=date.today().month, fecha_venta__year=date.today().year)
    for venta in ventas_mes:
        ingresos_mensuales += float(venta.total)
    nuevos_miembros = Miembro.objects.filter(fecha_registro__month=date.today().month,
                                             fecha_registro__year=date.today().year).count()
    membresias_vencidasl = Membresia.objects.filter(fecha_final__lt=date.today())
    membresias_vencidas = membresias_vencidasl.count()
    repetidos = Membresia.objects.values('miembro_id').annotate(conteo=Count('miembro_id')).filter(conteo__gt=1)
    membresias_vencidas -= repetidos.count()

    return JsonResponse({
        'membresias_activas': membresias_activas,
        'ingresos_mensuales': ingresos_mensuales,
        'nuevos_miembros': nuevos_miembros,
        'membresias_vencidas': membresias_vencidas
    })


# Para la grafica de membresias

from django.db.models.functions import ExtractYear, ExtractMonth


def distribucion_membresias(request):
    # Agrupar por tipo de membresía y contar cuántos miembros hay en cada tipo
    distribucion = (
        Membresia.objects.values('tipo_membresia__nombre')
        .annotate(total=Count('id'))
        .order_by('tipo_membresia__nombre')
    )
    # Preparar datos para la gráfica
    labels = [item['tipo_membresia__nombre'] for item in distribucion]
    data = [item['total'] for item in distribucion]
    return JsonResponse({'labels': labels, 'data': data})


def miembros_registrados_por_mes(request):
    # Agrupar miembros por año y mes de registro
    registros = (
        Miembro.objects.annotate(anio=ExtractYear('fecha_registro'), mes=ExtractMonth('fecha_registro'))
        .values('anio', 'mes')
        .annotate(total=Count('id'))
        .order_by('anio', 'mes')
    )
    # Preparar los datos para el frontend
    labels = [f"{item['anio']}-{item['mes']:02d}" for item in registros]  # Formato: Año-Mes
    data = [item['total'] for item in registros]
    return JsonResponse({'labels': labels, 'data': data})
