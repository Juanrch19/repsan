import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
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
    codigo = models.CharField(max_length=30, blank=True)
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Categoría")
    id_archivo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, verbose_name="Titulo")
    file = models.FileField(upload_to='documents/', verbose_name="Archivo")
    fecha_creacion = models.DateTimeField(default=datetime.datetime.now().replace(microsecond=0))
    numero_autoincrementable = models.IntegerField(default=1)

    def __str__(self):
        return self.titulo


    def save(self, *args, **kwargs):
        # Asegurarse de que siempre haya un código proporcionado por el usuario
        if not self.codigo:
            raise ValueError("El campo 'codigo' es obligatorio y debe ser proporcionado por el usuario.")

        # Incrementar el número autoincrementable solo si la categoría está presente, no es "caracterización" y no se ha asignado ya un número autoincrementable para esta categoría
        if self.categoria and self.categoria.nombre_categoria.lower() != 'caracterización' and self.numero_autoincrementable is None:
            # Obtener el número autoincrementable actual para esta categoría
            ultimo_numero = Document.objects.filter(categoria=self.categoria).aggregate(models.Max('numero_autoincrementable'))['numero_autoincrementable__max'] or 0
            self.numero_autoincrementable = ultimo_numero + 1

        # Agregar el número autoincrementable al código proporcionado por el usuario
        if self.numero_autoincrementable is not None:
            self.codigo = f"{self.codigo}-{self.numero_autoincrementable}"

     
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
    
        self.file.storage.delete(self.file.name)
        super().delete(using, keep_parents)


   