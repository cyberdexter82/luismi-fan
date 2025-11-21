# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

# Formulario para registrar usuarios (extiende el de Django)
class RegistroUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',) # Añadimos email si quieres

# Formulario para actualizar la foto de perfil
class ActualizarPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen'] # Solo queremos que puedan cambiar la imagen aquí