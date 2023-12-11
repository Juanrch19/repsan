import datetime
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=100,verbose_name="nombre_categoria")
    fecha_creacion = models.DateTimeField(default=datetime.datetime.now().replace(microsecond=0))

    def __str__(self):
        return self.nombre_categoria
    

class Proceso(models.Model):
    id_proceso = models.AutoField(primary_key=True)
    nombre_proceso = models.CharField(max_length=100,verbose_name="nombre_proceso")
    fecha_creacion = models.DateTimeField(default=datetime.datetime.now().replace(microsecond=0))

    def __str__(self):
        return self.nombre_proceso 
    
class Document(models.Model):
    proceso = models.ForeignKey(Proceso, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Proceso")
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Categoría")
    id_archivo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, verbose_name="Titulo")
    file = models.FileField(upload_to='documents/', verbose_name="Archivo")
    fecha_creacion = models.DateTimeField(default=datetime.datetime.now().replace(microsecond=0))
    def __str__(self):
        return self.titulo

    def delete(self, using=None, keep_parents=False):
        # Elimina el archivo asociado al documento
        self.file.storage.delete(self.file.name)
        super().delete(using, keep_parents)


    
class Codigo(models.Model):
    id_codigo = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    fecha_creacion = models.DateTimeField(default=datetime.datetime.now().replace(microsecond=0))

    def __str__(self):
        return self.codigo

   