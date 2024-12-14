from tkinter.font import names

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('miembros/', views.miembros_lista, name='miembros_lista'),
    path('miembros/crear/', views.crear_miembro_membresia, name='crear_miembro'),
    path('miembros/<int:pk>/actualizar/', views.actualizar_miembro, name='actualizar_miembro'),
    path('miembros/<int:pk>/asignar-membresia/', views.asignar_membresia, name='asignar_membresia'),
    path('registrar-asistencia/', views.registrar_asistencia, name='registrar_asistencia'),
    path('asistencias/', views.listar_asistencias, name='listar_asistencias'),

    path('tipos-membresia/', views.lista_tipos_membresia, name='lista_tipos_membresia'),
    path('tipos-membresia/crear/', views.crear_tipo_membresia, name='crear_tipo_membresia'),
    path('tipos-membresia/<int:pk>/actualizar/', views.actualizar_tipo_membresia, name='actualizar_tipo_membresia'),
    path('tipos-membresia/<int:pk>/eliminar/', views.eliminar_tipo_membresia, name='eliminar_tipo_membresia'),
    path('dashboard/', views.dashboard_data, name='dashboard'),

    # para la grafica de membresias
    path('distribucion-membresias/', views.distribucion_membresias, name='distribucion_membresias'),
    path('miembros-registrados-mes/', views.miembros_registrados_por_mes, name='miembros_registrados_por_mes'),

]
