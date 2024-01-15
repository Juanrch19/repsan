from django.contrib import admin
from django.contrib.auth.models import Permission
from repositorio.models import Categoria,Document,Proceso

# Register your models here.
admin.site.register(Permission)
admin.site.register(Categoria)
admin.site.register(Proceso)
admin.site.register(Document)
