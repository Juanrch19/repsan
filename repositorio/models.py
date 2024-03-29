import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.db.models.signals import post_delete
# Create your models here.


class Glosario(models.Model):
    id_termino = models.AutoField(primary_key=True)
    termino = models.CharField(max_length=150,verbose_name="termino")
    definicion = models.TextField(max_length=2000,verbose_name="definicion")

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
    file = models.FileField( max_length=200,upload_to='documents/', verbose_name="Archivo")
    fecha_creacion = models.DateTimeField(default=datetime.datetime.now().replace(microsecond=0))
    numero_autoincrementable = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        # Asegurarse de que siempre haya un código proporcionado por el usuario
        if not self.codigo:
            raise ValueError("El campo 'codigo_usuario' es obligatorio y debe ser proporcionado por el usuario.")

        # Obtener el objeto existente en la base de datos
        existing_obj = Document.objects.filter(id_archivo=self.id_archivo).first()

        # Si se está editando y se proporciona un nuevo archivo, eliminar el archivo antiguo
        if existing_obj and existing_obj.file != self.file:
            file_path = existing_obj.file.path
            default_storage.delete(file_path)

        categorias_incrementables = ['procedimiento', 'formato', 'manuales', 'diagrama']
        if self.categoria and self.categoria.nombre_categoria.lower() in categorias_incrementables:
            self.numero_autoincrementable = Document.objects.filter(categoria=self.categoria).aggregate(
                models.Max('numero_autoincrementable'))['numero_autoincrementable__max'] or 0 
            self.numero_autoincrementable += 1
        else:
            self.numero_autoincrementable = None  

        if self.numero_autoincrementable is not None:
            self.codigo = f"{self.codigo}"

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.file.storage.delete(self.file.name)
        super().delete(using, keep_parents)

# Eliminar el archivo al eliminar el objeto Document
@receiver(post_delete, sender=Document)
def delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        file_path = instance.file.path
        default_storage.delete(file_path)

