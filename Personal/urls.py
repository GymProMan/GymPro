from django.urls import path

from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index_personal'),  # Ruta para el index

    path('turnos/', views.listar_turnos, name='listar_turnos'),  # Listar turnos
    path('turnos/crear/', views.crear_turno, name='crear_turno'),  # Crear un nuevo turno
    path('turnos/modificar/<int:turno_id>/', views.modificar_turno, name='modificar_turno'),  # Modificar un turno
    path('turnos/eliminar/<int:turno_id>/', views.eliminar_turno, name='eliminar_turno'),  # Eliminar un turno
    path('personal/', views.listar_personal, name='listar_personal'),  # Vista para crear personal

    path('personal/modificar/<str:clave_f>/', views.modificar_personal, name='modificar_personal'),
    path('personal/eliminar/<str:clave_f>/', views.eliminar_personal, name='eliminar_personal'),
    path('personal/crear/', views.crear_personal, name='crear_personal'),  # Si tienes una vista de creación

    path('personal/marcar_salida/<int:asistencia_id>/', views.marcar_salida, name='marcar_salida'),

    path('personal/historial_asistencias/', views.historial_asistencias, name='historial_asistencias'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)