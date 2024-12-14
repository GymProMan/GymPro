from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index),
    path('leer/ap/',views.leer_aparato, name='leer_aparato'),
    path('leer/ap/crear/', views.crear_aparato, name='crear_aparato'),
    path('leer/cat/', views.leer_categoria, name='leer_categoria'),
    path('leer/cat/crear/', views.crear_categoria, name='crear_categoria'),
    path('leer/cat/modificar/<int:id>', views.modify_categoria, name='modificar_categoria'),
    path('leer/cat/eliminar/<int:id>', views.eliminar_categoria, name='eliminar_categoria'),
    path('leer/ap/modificar/<int:id>', views.modificar_aparato, name='modificar_aparato'),
    path('leer/ap/vincular/<int:id>', views.vincular_aparato, name='vincular_aparato'),

    path('leer/ap/eliminar/<int:id>', views.eliminar_aparato, name='eliminar_aparato'),
]