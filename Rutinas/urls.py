from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_miembros, name='listar_miembros'),
    path('rutina/crear/<int:miembro_id>/', views.crear_modificar_rutina,name='crear_modificar_rutina'),
    path('ejercicios/', views.listar_ejercicios, name='listar_ejercicios'),
    path('ejercicios/crear/', views.crear_ejercicio, name='crear_ejercicio'),
    path('mostrar_rutina/<str:clave>/', views.mostrar_rutina, name='mostrar_rutina'),
    path('rutinas/filtrar_ejercicios/', views.filtrar_ejercicios, name='filtrar_ejercicios'),
    path('rutinas/eliminar_ejercicio/', views.eliminar_ejercicio, name='eliminar_ejercicio'),
    path('rutinas/guardar_ejercicios/<str:clave>/', views.guardar_ejercicios, name='guardar_ejercicios'),
    path('rutinas/ver/<str:clave>/', views.ver_rutina, name='rutina_vista'),
    path('rutinas/eliminar/<str:clave>/', views.eliminar_rutina, name='eliminar_rutina'),


]