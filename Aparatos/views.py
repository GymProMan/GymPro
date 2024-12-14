from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import crearAparato, createCategoria,  vincular
import Aparatos
from Aparatos.models import Aparato, CategoriaAparato, CategoriaApa_Aparato


@login_required
def crear_aparato(request):
    if request.method == 'GET':
        return render(request, 'CrearAparato.html', {'form': crearAparato})
    else:
        # Convierte los valores de bandera y estado a booleanos
        bandera = request.POST.get('bandera') == 'true'
        estado = request.POST.get('estado') == 'true'

        # Crear el objeto Aparato con los datos del formulario
        Aparato.objects.create(
            nombre=request.POST['nombre'],
            descripcion=request.POST['descripcion'],
            cantidad=request.POST['cantidad'],
            bandera=bandera,
            tipo=request.POST['tipo'],
            ubicacion=request.POST['ubicacion'],
            estado=estado
        )

        # Redirigir con bandera de éxito
        return render(request, 'CrearAparato.html', {
            'form': crearAparato,
            'success': True  # Indicador de éxito
        })



@login_required
def eliminar_aparato(request,id):
    Aparato.objects.filter(idAparatos=id).delete()
    return redirect('leer_aparato')

@login_required
def modificar_aparato(request, id):
    # Recupera el aparato con el id dado o muestra un error 404 si no existe
    aparato = get_object_or_404(Aparato, idAparatos=id)

    if request.method == 'POST':
        # Convierte los valores de bandera y estado a booleanos
        bandera = request.POST.get('bandera') == 'true'
        estado = request.POST.get('estado') == 'true'

        # Actualiza los campos del aparato
        aparato.nombre = request.POST['nombre']
        aparato.descripcion = request.POST['descripcion']
        aparato.cantidad = request.POST['cantidad']
        aparato.bandera = bandera
        aparato.tipo = request.POST['tipo']
        aparato.ubicacion = request.POST['ubicacion']
        aparato.estado = estado

        # Guarda los cambios en la base de datos
        aparato.save()

        # Enviar indicador de éxito a la plantilla
        return render(request, 'ModificarAparato.html', {
            'form': crearAparato(initial={
                'nombre': aparato.nombre,
                'descripcion': aparato.descripcion,
                'cantidad': aparato.cantidad,
                'bandera': aparato.bandera,
                'tipo': aparato.tipo,
                'ubicacion': aparato.ubicacion,
                'estado': aparato.estado
            }),
            'success': True
        })
    else:
        # Prellenar el formulario con los valores actuales del aparato
        form = crearAparato(initial={
            'nombre': aparato.nombre,
            'descripcion': aparato.descripcion,
            'cantidad': aparato.cantidad,
            'bandera': aparato.bandera,
            'tipo': aparato.tipo,
            'ubicacion': aparato.ubicacion,
            'estado': aparato.estado
        })

        return render(request, 'ModificarAparato.html', {'form': form})


@login_required
def leer_aparato(request):
    aparatos= list(Aparato.objects.values())
    return render(request, 'Aparato.html', {'aparatos':aparatos})

@login_required
def leer_categoria(request):
    categorias= list(CategoriaAparato.objects.values())
    return render(request, 'Categoria.html', {'categorias':categorias})


@login_required
def crear_categoria(request):
    if request.method == 'GET':
        return render(request, 'CrearCategoria.html', {'form': createCategoria})
    else:
        # Crear la categoría
        CategoriaAparato.objects.create(nombre=request.POST['nombrecat'])

        # Redirigir con un indicador de éxito
        return render(request, 'CrearCategoria.html', {
            'form': createCategoria,
            'success': True  # Indicador de éxito para mostrar la alerta
        })


@login_required
def modify_categoria(request, id):
    # Recupera la categoría con el id correspondiente o muestra un error 404 si no existe
    categoria = get_object_or_404(CategoriaAparato, idCategoria=id)

    if request.method == "POST":
        # Instancia el formulario con los datos enviados por el usuario (POST)
        form = createCategoria(request.POST)
        if form.is_valid():
            # Actualiza el campo 'nombre' de la categoría con el dato del formulario
            categoria.nombre = form.cleaned_data['nombrecat']
            categoria.save()  # Guarda los cambios en la base de datos

            # Redirigir con indicador de éxito
            return render(request, 'ModificarCategoria.html', {
                'form': form,
                'success': True  # Indicador de éxito para mostrar la alerta
            })
    else:
        # Prellenar el formulario con el valor actual del campo 'nombre'
        form = createCategoria(initial={'nombrecat': categoria.nombre})

    # Renderiza la plantilla con el formulario prellenado
    return render(request, 'ModificarCategoria.html', {'form': form})


@login_required
def eliminar_categoria(request,id):
    CategoriaAparato.objects.filter(idCategoria=id).delete()
    return redirect('leer_categoria')

@login_required
def vincular_aparato(request, id):
    # Obtener el aparato por su ID
    aparato = get_object_or_404(Aparato, idAparatos=id)

    # Obtener todas las categorías
    categorias = CategoriaAparato.objects.all()

    # Si no hay categorías, renderiza la página con un mensaje de error
    if not categorias.exists():
        return render(request, 'VincularCategorias.html', {'form': None, 'error': 'No hay categorías disponibles.'})

    # Crear las opciones para el combo box
    categoria_combo = [(categoria.idCategoria, categoria.nombre) for categoria in categorias]

    # Inicializar el formulario
    form = vincular(initial={'idAparatos': id})
    form.fields['categorias'].choices = categoria_combo  # Asignar las opciones al campo 'categorias'

    # Si el método es POST (el formulario fue enviado)
    if request.method == 'POST':
        # Inicializar el formulario con los datos enviados
        form = vincular(request.POST)
        form.fields['categorias'].choices = categoria_combo  # Asignar las opciones antes de validar

        # Verificar si el formulario es válido
        if form.is_valid():
            # Extraer los datos del formulario
            id_categoria = form.cleaned_data['categorias']
            id_aparato = form.cleaned_data['idAparatos']

            aparato_instance = get_object_or_404(Aparato, idAparatos=id_aparato)
            categoria_instance = get_object_or_404(CategoriaAparato, idCategoria=id_categoria)

            # Crear una nueva vinculación entre aparato y categoría
            CategoriaApa_Aparato.objects.create(idAparato=aparato_instance, idCategoria=categoria_instance)

            # Redirigir después de guardar con el mensaje de éxito
            return render(request, 'VincularCategorias.html', {
                'form': form,
                'aparato': aparato,
                'success': True  # Indicador de éxito
            })

    # Renderizar el formulario para GET o en caso de error
    return render(request, 'VincularCategorias.html', {'form': form, 'aparato': aparato})
