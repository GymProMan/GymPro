"""
URL configuration for GYM_PRO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.http import HttpResponseRedirect
from django.urls import path, include
import Miembros

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: HttpResponseRedirect('usuarios/my_login')),
    path('miembros/', include('Miembros.urls')),
    path('usuarios/', include('crm.urls')),
    path('aparatos/', include('Aparatos.urls')),
    path('productos/', include('Ventas_Compras.urls')),
    path('personal/', include('Personal.urls')),
    path('rutinas/', include('Rutinas.urls')),
    path('movil/', include('Movil.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
