from django import forms
from .models import Categoria, Document, Proceso
from django.contrib.auth.forms import SetPasswordForm


class UserRequestForm(forms.Form):
    full_name = forms.CharField(label='Nombre completo', max_length=100)
    email = forms.EmailField(label='Correo electronico')
    reason = forms.CharField(label='Motivo de la solicitud',widget=forms.Textarea)

    
class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ['nombre_categoria']
    def save(self, commit=True):
        super().save(commit)

class ProcesoForm(forms.ModelForm):
    class Meta:
        model = Proceso
        fields = ['nombre_proceso']
    def save(self, commit=True):
        super().save(commit)


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['proceso','codigo','categoria', 'titulo', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Añade una lista desplegable con todas las categorías disponibles
        self.fields['categoria'] = forms.ModelChoiceField(
            queryset=Categoria.objects.all(),
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Categoría'
        )

        # Añade una lista desplegable con todos los procesos disponibles
        self.fields['proceso'] = forms.ModelChoiceField(
            queryset=Proceso.objects.all(),
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Proceso'
        )
        
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="",
    )

    new_password2 = forms.CharField(
        label='Confirmar Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="",
    )