from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from usuarios import views as user_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas Principales
    path('', views.vista_inicio, name='inicio'),
    path('musica/', views.vista_musica, name='musica_disponible'),
    path('proximamente/', views.vista_proximamente, name='proximamente'),
    path('20anos/', views.vista_album_20, name='album_20'),
    path('romance/', views.vista_album_romance, name='album_romance'),
    path('2010/', views.vista_album_2010, name='album_2010'),

    # Rutas de Usuario (Directas aquí, sin usar include)
    path('registro/', user_views.registro, name='registro'),
    path('perfil/', user_views.perfil, name='perfil'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),
]

# Configuración para ver fotos en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)