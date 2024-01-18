from django.contrib import admin
from .models import Document
from django.contrib.auth.models import Permission
from repositorio.models import Categoria,Document,Proceso

# Register your models here.

class DocumentAdmin(admin.ModelAdmin):
    search_fields = ['proceso__nombre_proceso','codigo','titulo','categoria__nombre_categoria']
admin.site.register(Document, DocumentAdmin)

class ProcesoAdmin(admin.ModelAdmin):
    search_fields = ['nombre_proceso']
admin.site.register(Proceso, ProcesoAdmin)

class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ['nombre_categoria']
admin.site.register(Categoria, CategoriaAdmin)

admin.site.register(Permission)

