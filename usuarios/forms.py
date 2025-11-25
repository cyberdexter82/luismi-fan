from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil

# Formulario para registrar usuarios (extiende el de Django)
class RegistroUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Añadimos el campo email al registro estándar
        fields = UserCreationForm.Meta.fields + ('email',)

# Formulario para editar el perfil (Foto)
class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        # IMPORTANTE: Debe llamarse 'foto' porque así se llama en tu base de datos (models.py)
        fields = ['foto']