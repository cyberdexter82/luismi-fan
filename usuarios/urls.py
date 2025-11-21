# usuarios/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as usuario_views

urlpatterns = [
    # Rutas propias que creamos en views.py
    path('registro/', usuario_views.registro, name='registro'),
    path('perfil/', usuario_views.perfil, name='perfil'),
    
    # Vista de LOGIN (Usamos tu plantilla login.html)
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    
    # Vista de LOGOUT (Aquí está el truco: next_page='inicio')
    # Esto hace que al cerrar sesión, te mande directo a la página principal
    path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),
]