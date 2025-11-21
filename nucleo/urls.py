from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Inicio
    path('', views.vista_inicio, name='inicio'),

    # Menús
    path('musicadisponible.html', views.vista_musica, name='musica_disponible'),
    path('proximamente.html', views.vista_proximamente, name='proximamente'),

    # Álbumes
    path('20anos/', views.vista_album_20, name='album_20'),
    path('romance/', views.vista_album_romance, name='album_romance'),
    path('2010/', views.vista_album_2010, name='album_2010'),

    # --- INCLUSIÓN DE USUARIOS Y AUTENTICACIÓN ---
    # 1. Vistas personalizadas de la app 'usuarios' (Perfil, Registro)
    path('usuarios/', include('usuarios.urls')), 
    
    # 2. Vistas nativas de Django (Login, Logout, etc.) <--- ¡ESTA ES LA LÍNEA CRUCIAL!
    path('auth/', include('django.contrib.auth.urls')), 
    # -----------------------------------------------
]

# Configuración para ver las imágenes en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)