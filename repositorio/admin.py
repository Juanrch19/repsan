from django.contrib import admin
from .models import Document
from django.contrib.auth.models import Permission
from repositorio.models import Categoria,Document,Proceso,Glosario

# Register your models here.
class GlosarioAdmin(admin.ModelAdmin):
    search_fields = ['termino']
    list_display = ['termino','definicion']
admin.site.register(Glosario,GlosarioAdmin)

class DocumentAdmin(admin.ModelAdmin):
    search_fields = ['proceso__nombre_proceso','codigo','titulo','categoria__nombre_categoria']
    list_display = ['proceso', 'codigo','titulo', 'categoria','fecha_creacion']
    exclude = ['numero_autoincrementable']
admin.site.register(Document, DocumentAdmin)

class ProcesoAdmin(admin.ModelAdmin):
    search_fields = ['nombre_proceso']
    list_display = ['nombre_proceso','fecha_creacion']
admin.site.register(Proceso, ProcesoAdmin)

class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ['nombre_categoria']
    list_display = ['nombre_categoria','fecha_creacion']
admin.site.register(Categoria, CategoriaAdmin)

admin.site.register(Permission)

