from django.contrib import admin

from repositorio.models import Categoria,Document,Proceso

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Proceso)
admin.site.register(Document)
