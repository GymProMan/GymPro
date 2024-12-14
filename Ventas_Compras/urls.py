from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_ventas, name='index_ventas'),
    path('listar', views.listar_productos, name='listar_productos'),
    path('crear/', views.crear_productos, name='crear_producto'),
    path('editar/<int:pk>/', views.editar_productos, name='editar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_productos, name='eliminar_producto'),
    path('listar_proveedores/', views.listar_proveedores, name='listar_proveedores'),
    path('crear_proveedor/', views.crear_proveedor, name='crear_proveedor'),
    path('editar_proveedor/<int:pk>/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar_proveedor/<int:pk>', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('compras/', views.registrar_compra, name='registrar_compra'),
    path('listar_compras', views.listar_compras, name='listar_compras'),
    path('listar_compras/<int:compra_id>/', views.detalle_compra, name='detalle_compra'),
    path('ventas/', views.registrar_venta, name='registrar_venta'),
    path('listar_ventas', views.listar_ventas, name='listar_ventas'),
    path('listar_ventas/<int:venta_id>/<str:tipo>', views.detalle_venta, name='detalle_venta'),

    # agregado por mi luis
    path('ingresos-totales-mes/', views.ingresos_totales_por_mes, name='ingresos_totales_por_mes'),
    path('stock-productos/', views.stock_productos, name='stock_productos'),
]
