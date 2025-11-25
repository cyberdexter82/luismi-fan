from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    # Relación 1 a 1 con el usuario estándar de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # --- CORRECCIÓN: Lo renombramos a 'foto' para que coincida con forms.py ---
    foto = models.ImageField(default='default.jpg', upload_to='fotos_perfil')

    def __str__(self):
        return f'Perfil de {self.usuario.username}'

# --- SEÑALES (Para crear el perfil automáticamente) ---
@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, **kwargs):
    instance.perfil.save()