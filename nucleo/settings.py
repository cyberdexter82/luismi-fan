"""
Django settings for nucleo project.
Configuración Híbrida: Local (SQLite) / Producción (Azure PostgreSQL)
"""

from pathlib import Path
import os
import mimetypes
import dj_database_url

# 1. Rutas Base
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Seguridad
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-clave-desarrollo-local-12345')

# DEBUG inteligente:
# Se apaga solo en Azure (si existe la variable WEBSITE_HOSTNAME)
DEBUG = 'WEBSITE_HOSTNAME' not in os.environ

# Permitir todos los hosts (necesario para Azure)
ALLOWED_HOSTS = ['*']

# 3. Aplicaciones Instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Librería para probar estáticos en local como en producción
    'whitenoise.runserver_nostatic',
    # Tu App de usuarios
    'usuarios',
]

# 4. Middleware (Intermediarios)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--- VITAL: Sirve CSS/JS en la nube
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nucleo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nucleo.wsgi.application'

# 5. Base de Datos (Configuración Inteligente)
# Busca la variable 'DATABASE_URL' en Azure. Si no está, usa SQLite local.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# 6. Validadores de Contraseña
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# 7. Idioma y Zona Horaria
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 8. Archivos Estáticos (CSS, JS, Imágenes del diseño)
STATIC_URL = '/static/'

# Origen: Dónde están tus archivos en la PC
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Destino: Dónde los pone collectstatic para la nube
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Motor de almacenamiento: Usamos CompressedStaticFilesStorage (sin Manifest)
# para evitar errores 404 si falta algún archivo.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# 9. Archivos Multimedia (Fotos de perfil)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 10. Redirecciones
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'inicio'
LOGIN_URL = 'login'

# 11. Seguridad CSRF para Azure (VITAL PARA FORMULARIOS)
# Esto arregla el error 403 "Forbidden"
CSRF_TRUSTED_ORIGINS = [
    'https://luismi-fan-app-2025-bgccc0dwazdahvhc.canadacentral-01.azurewebsites.net',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Parche para Windows
mimetypes.add_type("text/css", ".css", True)