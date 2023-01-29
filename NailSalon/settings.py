"""
Django settings for NailSalon project.
Generated by 'django-admin startproject' using Django 4.1.
For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os.path
from pathlib import Path



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path (__file__).resolve ( ).parent.parent
AUTH_USER_MODEL = 'Account.User'

MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
MEDIA_URL = ''

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-d4!6d0)!)(5!__6li(6b(sc9=d^xrnu*gns$^^6pzf#9s=9p+("

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TIME_INPUT_FORMATS = ('%I:%M %p')

ALLOWED_HOSTS = ['127.0.0.1',
                 '.pythonanywhere.com']

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    'Account.apps.AccountConfig',
    'Scheduling.apps.SchedulingConfig',
    'Appointments.apps.AppointmentsConfig',
    'cart.apps.CartConfig',
    'Calendar.apps.CalendarConfig',
    'Manager.apps.ManagerConfig',
    
    'django_crontab',
    'django_behave',
]

CRONTAB_COMMAND_SUFFIX = '2>&1'
CRONJOBS = [
    ('0 9 * * 1-6', 'helper.cron.newday_open_job', f">> {os.path.join (BASE_DIR, 'NailSalon/log/helper_job.log')}"),
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "NailSalon.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join (BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cart.context_processors.cart",
                "Scheduling.context_processors.getTodaysDate",
                "Calendar.context_processors.buildCalendar"
            ],
            "libraries":{
                "extra_tags": "Manager.templatetags.extra_tags"
            }
        },
    },
]

WSGI_APPLICATION = "NailSalon.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_TZ = True

TIME_INPUT_FORMATS = ('%I:%M %p')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = '../'
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/'

CART_SESSION_ID = 'cart'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TEST_RUNNER = 'django_behave'

# SMTP Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'applenailsalon23@gmail.com'
EMAIL_HOST_PASSWORD = 'shhanovesnoumvov'
