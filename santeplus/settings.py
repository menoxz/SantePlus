"""
Django settings for santeplus project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ffah%*6^u2q=3mbm^-d+b!n(gq_l(16fo7%@np=)a3!(a8k-g!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'koumaglo_utilisateurs.apps.KoumagloUtilisateursConfig',
    'koumaglo_patients.apps.KoumagloPatientsConfig',
    'koumaglo_medecins.apps.KoumagloMedecinsConfig',
    'koumaglo_consultations.apps.KoumagloConsultationsConfig',
    'koumaglo_ordonnances.apps.KoumagloOrdonnancesConfig',
    'koumaglo_factures.apps.KoumagloFacturesConfig',
    'koumaglo_parametres.apps.KoumagloParametresConfig',
    'axes',  # Django Axes pour le verrouillage des comptes
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",  # Django Axes middleware
]

ROOT_URLCONF = "santeplus.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = "santeplus.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'santeplus_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication
AUTH_USER_MODEL = 'koumaglo_utilisateurs.Utilisateur'

LOGIN_REDIRECT_URL = 'koumaglo_utilisateurs:dashboard'
LOGOUT_REDIRECT_URL = 'koumaglo_utilisateurs:login'
LOGIN_URL = 'koumaglo_utilisateurs:login'

# Configuration pour django-axes (verrouillage des comptes)
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Configuration de django-axes
AXES_FAILURE_LIMIT = 5  # Nombre de tentatives avant verrouillage
AXES_COOLOFF_TIME = 1  # Durée du verrouillage en heures
AXES_LOCKOUT_TEMPLATE = 'registration/lockout.html'  # Template pour le verrouillage
AXES_LOCKOUT_PARAMETERS = ['username']  # Verrouillage basé sur le nom d'utilisateur
AXES_RESET_ON_SUCCESS = True  # Réinitialiser le compteur après une connexion réussie
AXES_ENABLE_ADMIN = True  # Activer le tableau de bord admin

# Configuration des sessions
SESSION_COOKIE_AGE = 3600  # Durée de la session en secondes (1 heure)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Expirer la session à la fermeture du navigateur
SESSION_SAVE_EVERY_REQUEST = True  # Mettre à jour la date d'expiration à chaque requête
