from django.contrib import admin
from django.urls import path, include # <--- 1. IMPORTANTE: AGREGAR include AQUÍ
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

    # --- 2. IMPORTANTE: ESTA ES LA LÍNEA QUE TE FALTA ---
    # Esto conecta tus nuevas vistas de registro y login
    path('usuarios/', include('usuarios.urls')), 
]

# Configuración para ver las imágenes en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)