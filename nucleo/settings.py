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
# Intenta leer la llave secreta de las variables de entorno (Azure).
# Si no existe, usa una clave por defecto para desarrollo local.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-clave-desarrollo-local-12345')

# DEBUG inteligente:
# Si estamos en Azure (existe la variable WEBSITE_HOSTNAME), se apaga (False).
# Si estamos en tu PC (no existe esa variable), se enciende (True).
DEBUG = 'WEBSITE_HOSTNAME' not in os.environ

# Permitir todos los hosts (necesario para que Azure funcione con cualquier dominio)
ALLOWED_HOSTS = ['*']

# 3. Aplicaciones Instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps de terceros
    'whitenoise.runserver_nostatic', # Ayuda a servir estáticos en modo local también
    # Mis Apps
    'usuarios', # Tu app de registro, login y perfiles
]

# 4. Middleware (Intermediarios)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--- VITAL: Sirve CSS/JS/Imágenes en la nube
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
        # Carpeta donde guardas tus HTML
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
# Busca la variable 'DATABASE_URL' en el entorno (Azure).
# Si la encuentra, se conecta a PostgreSQL.
# Si no la encuentra (tu PC), usa el archivo db.sqlite3 local.
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

# Dónde busca Django los archivos en tu proyecto (origen)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Dónde los junta todos para la nube (destino)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Motor de almacenamiento optimizado para la nube (WhiteNoise)
# Usamos CompressedManifestStaticFilesStorage para máxima eficiencia
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 9. Archivos Multimedia (Fotos de perfil subidas por usuarios)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 10. Redirecciones del sistema de login
LOGIN_REDIRECT_URL = 'inicio'  # A dónde ir después de iniciar sesión
LOGOUT_REDIRECT_URL = 'inicio' # A dónde ir después de cerrar sesión
LOGIN_URL = 'login'            # A dónde ir si intentan ver el perfil sin permiso

# 11. Ajustes Finales
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Parche para que Windows reconozca correctamente los archivos CSS
mimetypes.add_type("text/css", ".css", True)