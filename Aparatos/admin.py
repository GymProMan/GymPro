from django.contrib import admin
from .models import Aparato,CategoriaAparato,CategoriaApa_Aparato

# Register your models here.

admin.site.register(Aparato)
admin.site.register(CategoriaAparato)
admin.site.register(CategoriaApa_Aparato)