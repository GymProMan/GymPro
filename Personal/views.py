from cloudinary.uploader import upload
from django.shortcuts import render, redirect, get_object_or_404

from GYM_PRO import settings
from .models import Turno, Asistencia
from .models import Personal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import PersonalForm
from .forms import TurnoForm
from datetime import datetime


def index(request):
    mensaje = ""

    if request.method == 'POST':
        clave = request.POST.get('clave')  # Obtiene la clave del personal enviada por el formulario
        try:
            personal = Personal.objects.get(clave=clave)  # Busca el personal por su clave
            now = datetime.now().time()  # Hora actual

            # Verifica si la hora actual está dentro de las horas de su turno
            if personal.turno.hora_inicio <= personal.turno.hora_final:
                # Caso normal: el turno está en el mismo día (ej: 7am a 3pm)
                if personal.turno.hora_inicio <= now <= personal.turno.hora_final:
                    mensaje = f"Acceso permitido. Bienvenido {personal.nombre} {personal.apellido}."
                    registrar_asistencia(personal)
                else:
                    mensaje = "Acceso denegado. Fuera del horario de turno."
            else:
                # Caso turno cruza medianoche (ej: 10pm a 6am)
                if now >= personal.turno.hora_inicio or now <= personal.turno.hora_final:
                    mensaje = f"Acceso permitido. Bienvenido {personal.nombre} {personal.apellido}."
                    registrar_asistencia(personal)
                else:
                    mensaje = "Acceso denegado. Fuera del horario de turno."
        except Personal.DoesNotExist:
            mensaje = "Clave incorrecta. No existe ningún empleado con esa clave."

    # Listar el personal que ya ha registrado su asistencia en el día actual y que aún no han marcado su salida
    asistencias = Asistencia.objects.filter(fecha=datetime.today(), hora_salida__isnull=True)

    # Renderizar la plantilla con el mensaje y las asistencias activas
    return render(request, 'index_personal.html', {'mensaje': mensaje, 'asistencias': asistencias})


def registrar_asistencia(personal):
    """Registra la hora de entrada para el personal si aún no lo ha hecho hoy."""
    asistencia, created = Asistencia.objects.get_or_create(
        personal=personal,
        fecha=datetime.today(),
        defaults={'hora_entrada': datetime.now().time()}
    )
    if not created:
        # Si ya existe el registro para hoy, no lo modifica
        pass


def marcar_salida(request, asistencia_id):
    asistencia = get_object_or_404(Asistencia, id_asistencia=asistencia_id)
    asistencia.marcar_salida()
    return redirect('index_personal')


# views.py

from django.shortcuts import render
from .models import Personal, Asistencia


def historial_asistencias(request):
    asistencias = None
    empleado_nombre = None  # Variable para almacenar el nombre completo del empleado

    if request.method == 'POST':
        clave = request.POST.get('clave')  # Obtener la clave ingresada

        if clave:
            # Buscar al empleado por clave
            try:
                empleado = Personal.objects.get(clave=clave)
                empleado_nombre = f"{empleado.nombre} {empleado.apellido}"  # Almacenar el nombre completo
                asistencias = Asistencia.objects.filter(personal=empleado).order_by('-fecha')
                if not asistencias.exists():
                    print("No se encontraron asistencias para el empleado.")
            except Personal.DoesNotExist:
                print("No se encontró un empleado con esa clave.")

    return render(request, 'historial_asistencias.html',
                  {'asistencias': asistencias, 'empleado_nombre': empleado_nombre})


def crear_turno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_turnos')  # Redirige a la página principal después de crear el turno
    else:
        form = TurnoForm()
    return render(request, 'crear_turno.html', {'form': form})


def listar_turnos(request):
    turnos = Turno.objects.all()  # Obtener todos los turnos
    return render(request, 'listar_turnos.html', {'turnos': turnos})


def modificar_turno(request, turno_id):
    turno = get_object_or_404(Turno, id_turno=turno_id)  # Obtener el turno existente por su ID

    if request.method == 'POST':
        form = TurnoForm(request.POST, instance=turno)  # Cargar los datos en el formulario
        if form.is_valid():
            form.save()  # Guardar los cambios
            return redirect('listar_turnos')  # Redirigir después de guardar
    else:
        form = TurnoForm(instance=turno)  # Pre-cargar el formulario con los datos del turno

    return render(request, 'modificar_turno.html', {'form': form, 'turno': turno})


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from .models import Turno, Personal  # Asegúrate de importar los modelos adecuados


@csrf_exempt
def eliminar_turno(request, turno_id):
    if request.method == 'POST':
        turno = get_object_or_404(Turno, id_turno=turno_id)

        # Verificar si el turno está asignado a algún personal
        personal_asignado = Personal.objects.filter(turno=turno).exists()
        if personal_asignado:
            return JsonResponse({
                'success': False,
                'mensaje': 'No se puede eliminar el turno porque está asignado a personal.'
            }, status=400)

        # Si no está asignado, eliminar el turno
        turno.delete()
        return JsonResponse({'success': True, 'mensaje': 'Turno eliminado con éxito.'})
    else:
        return JsonResponse({'success': False, 'mensaje': 'Método no permitido.'}, status=405)


def crear_personal(request):
    if request.method == 'POST':

        form = PersonalForm(request.POST, request.FILES)
        if form.is_valid():
            if 'foto' in request.FILES:
                Personal.foto = request.FILES['foto']
                try:
                    result = upload(request.FILES['foto'],
                                    cloud_name=settings.CLOUDINARY_STORAGE.get('CLOUDINARY_CLOUD_NAME'),
                                    api_key=settings.CLOUDINARY_STORAGE.get('CLOUDINARY_API_KEY'),
                                    api_secret=settings.CLOUDINARY_STORAGE.get('CLOUDINARY_API_SECRET'))
                except Exception as e:
                    print(f"Error al subir la imagen: {e}")
                Personal.foto_cloud = result['secure_url']
            form.save()
            return redirect('listar_personal')  # Redirige al index después de crear el personal
    else:
        form = PersonalForm()
    return render(request, 'crear_personal.html', {'form': form})


def listar_personal(request):
    personal_list = Personal.objects.all()  # Obtener todo el personal
    return render(request, 'listar_personal.html', {'personal_list': personal_list})


def modificar_personal(request, clave_f):
    personal = get_object_or_404(Personal, clave=clave_f)

    if request.method == 'POST':
        form = PersonalForm(request.POST, request.FILES, instance=personal)
        if form.is_valid():
            form.save()
            return redirect('listar_personal')  # Redirige al listado de personal
    else:
        form = PersonalForm(instance=personal)

    return render(request, 'modificar_personal.html', {'form': form, 'personal': personal})


def eliminar_personal(request, clave_f):
    # Obtener el personal por su clave
    persona = get_object_or_404(Personal, clave=clave_f)
    if request.method == 'POST':
        persona.delete()
        return JsonResponse({'success': True, 'mensaje': 'Personal eliminado con éxito.'})
    return JsonResponse({'success': False, 'mensaje': 'Método no permitido.'}, status=405)
