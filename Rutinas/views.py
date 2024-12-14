from sqlite3 import OperationalError

from cloudinary.uploader import upload
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from GYM_PRO import settings
from .models import Rutina, RutinaEjercicio
from .models import Ejercicios
from Miembros.models import Miembro

# Vista para listar y filtrar miembros


from Aparatos.models import Aparato


def crear_ejercicio(request):
    aparatos = Aparato.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        categoria = request.POST.get('categoria')
        ejecucion = request.POST.get('ejecucion')
        guia = request.POST.get('guia')
        nombre_aparato = request.POST.get('id_aparato')

        if not nombre_aparato:
            return render(request, 'crear_ejercicio.html',
                          {'aparatos': aparatos, 'error': 'Debe seleccionar un aparato.'})

        try:

            aparato = Aparato.objects.get(nombre=nombre_aparato)
        except Aparato.DoesNotExist:
            aparato = None

        ejercicio = Ejercicios(
            nombre=nombre,
            categoria=categoria,
            ejecucion=ejecucion,
            guia=guia,
            id_aparato=aparato
        )

        if 'foto' in request.FILES:
            ejercicio.foto = request.FILES['foto']
            try:
                result = upload(request.FILES['foto'],  # Pass the actual file data
                                cloud_name=settings.CLOUDINARY_STORAGE.get('CLOUDINARY_CLOUD_NAME'),
                                api_key=settings.CLOUDINARY_STORAGE.get('CLOUDINARY_API_KEY'),
                                api_secret=settings.CLOUDINARY_STORAGE.get('CLOUDINARY_API_SECRET'))
                ejercicio.foto_cloud = result['secure_url']
            except Exception as e:
                print(f"Error al subir la imagen: {e}")

        ejercicio.save()
        return redirect('listar_ejercicios')

    return render(request, 'crear_ejercicio.html', {'aparatos': aparatos})


def listar_miembros(request):
    miembros = Miembro.objects.all()
    clave = request.GET.get('clave', '')

    if clave:
        miembros = miembros.filter(clave__icontains=clave)

    for miembro in miembros:
        miembro.tiene_rutina = Rutina.objects.filter(id_miembro=miembro).exists()

        # Si tiene rutina, verificar si tiene ejercicios asociados
        if miembro.tiene_rutina:
            rutina = Rutina.objects.get(id_miembro=miembro)
            miembro.rutina_tiene_ejercicios = RutinaEjercicio.objects.filter(id_rutina=rutina).exists()
        else:
            miembro.rutina_tiene_ejercicios = False

    return render(request, 'listar_miembros.html', {'miembros': miembros, 'clave': clave})


def crear_modificar_rutina(request, miembro_id):
    miembro = get_object_or_404(Miembro, clave=miembro_id)
    rutina = Rutina.objects.filter(id_miembro=miembro).first()  # Busca si ya existe una rutina

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        objetivo = request.POST.get('objetivo')
        nota = request.POST.get('nota')

        if rutina:  # Si ya existe una rutina, actualízala
            rutina.nombre = nombre
            rutina.objetivo = objetivo
            rutina.nota = nota
            rutina.save()
        else:  # Si no existe, créala
            Rutina.objects.create(
                id_miembro=miembro,
                nombre=nombre,
                objetivo=objetivo,
                nota=nota,
            )
        return redirect('listar_miembros')

    return render(request, 'crear_rutina.html', {'miembro': miembro, 'rutina': rutina})


def listar_ejercicios(request):
    ejercicios = Ejercicios.objects.all()  # Obtener todos los ejercicios
    return render(request, 'listar_ejercicios.html', {'ejercicios': ejercicios})


def mostrar_rutina(request, clave):
    miembro = Miembro.objects.get(clave=clave)
    rutina = Rutina.objects.get(id_miembro=miembro)
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    categorias = ["Pierna", "Espalda", "Glúteo", "Pecho", "Hombro", "Abdomen", "Bíceps", "Tríceps", "Antebrazo"]
    ejercicios = Ejercicios.objects.all()
    if 'rutina_carrito' not in request.session:
        request.session['rutina_carrito'] = {dia: [] for dia in dias}
    if request.method == "POST":
        dia = request.POST.get('dia')
        ejercicio_id = request.POST.get('ejercicio_id')
        series = request.POST.get('series')
        repeticiones = request.POST.get('repeticiones')
        if dia and ejercicio_id:
            ejercicio = Ejercicios.objects.get(nombre=ejercicio_id)
            ejercicios_dia = request.session['rutina_carrito'][dia]
            if any(ej['nombre'] == ejercicio.nombre for ej in ejercicios_dia):
                messages.error(request, f"El ejercicio '{ejercicio.nombre}' ya está asignado al día {dia}.")
            else:
                request.session['rutina_carrito'][dia].append({
                    "nombre": ejercicio.nombre,
                    "categoria": ejercicio.categoria,
                    "series": series,
                    "repeticiones": repeticiones,
                    "foto": ejercicio.foto.url,
                })
                request.session.modified = True
                messages.success(request, f"Ejercicio '{ejercicio.nombre}' agregado al día {dia}.")
    return render(request, 'mostrar_rutina.html', {
        'miembro': miembro,
        'rutina': rutina,
        'dias': dias,
        'ejercicios': ejercicios,
        'categorias': categorias,
        'carrito': request.session.get('rutina_carrito', [])
    })


def eliminar_ejercicio(request):
    if request.method == 'POST':
        dia = request.POST.get('dia')
        ejercicio_nombre = request.POST.get('ejercicio_nombre')
        clave = request.POST.get('clave')

        if 'rutina_carrito' in request.session:
            carrito = request.session['rutina_carrito']
            if dia in carrito:
                carrito[dia] = [ej for ej in carrito[dia] if ej["nombre"] != ejercicio_nombre]
                request.session['rutina_carrito'] = carrito
                request.session.modified = True

    return redirect(f'http://127.0.0.1:8000/rutinas/mostrar_rutina/{clave}/')


def filtrar_ejercicios(request):
    categoria = request.GET.get('categoria', '')
    ejercicios = Ejercicios.objects.filter(categoria=categoria)
    data = [{'id': e.id_ejercicio, 'nombre': e.nombre} for e in ejercicios]
    return JsonResponse(data, safe=False)


from django.contrib import messages


def guardar_ejercicios(request, clave):
    miembro = get_object_or_404(Miembro, clave=clave)
    rutina = get_object_or_404(Rutina, id_miembro=miembro)

    carrito = request.session.get('rutina_carrito', {})
    if not carrito:
        messages.error(request, "No hay ejercicios en el carrito para guardar.")
        return redirect('mostrar_rutina', clave=clave)

    for dia, ejercicios in carrito.items():
        for ejercicio in ejercicios:
            ejercicio_obj = Ejercicios.objects.filter(nombre=ejercicio['nombre']).first()
            if ejercicio_obj:
                RutinaEjercicio.objects.create(
                    id_rutina=rutina,
                    id_ejercicio=ejercicio_obj,
                    dia=dia,
                    nombre=ejercicio['categoria'],
                    series=ejercicio['series'],
                    repeticiones=ejercicio['repeticiones']
                )

    # Limpiar el carrito después de guardar
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    request.session['rutina_carrito'] = {dia: [] for dia in dias}
    request.session.modified = True

    # Agregar mensaje de éxito
    messages.success(request, "Rutina creada con éxito.")
    return redirect('listar_miembros')


def ver_rutina(request, clave):
    miembro = get_object_or_404(Miembro, clave=clave)

    rutina = get_object_or_404(Rutina, id_miembro=miembro)

    ejercicios_por_dia = {dia: [] for dia in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]}
    ejercicios_rutina = RutinaEjercicio.objects.filter(id_rutina=rutina)

    for ejercicio in ejercicios_rutina:
        ejercicios_por_dia[ejercicio.dia].append(ejercicio)

    return render(request, 'rutina_vista.html', {
        'miembro': miembro,
        'ejercicios_por_dia': ejercicios_por_dia,
    })


def eliminar_rutina(request, clave):
    miembro = get_object_or_404(Miembro, clave=clave)
    rutina = get_object_or_404(Rutina, id_miembro=miembro)
    RutinaEjercicio.objects.filter(id_rutina=rutina).delete()

    return redirect('listar_miembros')
