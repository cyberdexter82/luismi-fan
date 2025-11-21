"""
Django settings for nucleo project.
"""

from pathlib import Path
import os
import dj_database_url # Importado para leer la URL de Azure/Postgres

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings
SECRET_KEY = 'django-insecure-x*n)_ah0h3%z)3v%8-@e$2$@+=9naui4h-e7-)2uk5-a5)'

# --- CONFIGURACIÓN DE PRODUCCIÓN / AZURE ---
DEBUG = True 
# Cambia 'tu_app_azure.azurewebsites.net' por el dominio real de Azure
# O por '*' si necesitas que acepte cualquier host (menos seguro)
ALLOWED_HOSTS = ['tu_dominio.azurewebsites.net', '127.0.0.1'] 
# ------------------------------------------

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--- AÑADIDO: Para servir CSS en Azure
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

# ----------------------------------------------------------------------
# Database (POSTGRESQL / AZURE READY)
# ----------------------------------------------------------------------
# Si encuentra la variable de entorno DATABASE_URL (que pondremos en Azure),
# usa PostgreSQL. Si no, usa SQLite localmente.
DATABASE_URL = os.getenv("DATABASE_URL") 

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600, conn_health_check=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
# ----------------------------------------------------------------------

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# ----------------------------------------------------------------------
STATIC_URL = 'static/'

# VITAL: Carpeta donde Django buscará archivos estáticos (origen)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# VITAL PARA PRODUCCIÓN (AZURE/WHITENOISE)
# 1. Carpeta de destino donde collectstatic reunirá todo (DEBE SER ÚNICA)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

# 2. Motor de almacenamiento que sirve los archivos estáticos con WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 
# ----------------------------------------------------------------------


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# VITAL: Parche para que Windows cargue bien el CSS
import mimetypes
mimetypes.add_type("text/css", ".css", True)

# Al final del archivo, asegúrate de tener esto para las fotos de perfil:
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Redirección al iniciar/cerrar sesión
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'inicio'