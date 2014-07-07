"""
Django settings for TenniSoda project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
#email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'wuhaochen1990@gmail.com'
EMAIL_HOST_PASSWORD = '199012228711'
EMAIL_PORT = 587

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.getcwd()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%79*1l80dzwkblp7e_-%np-+8yd53^i=_90$cy0thhg)rhnudu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Template direction

TEMPLATE_DIRS = (
        os.path.join(PROJECT_DIR,'templates/'),
        os.path.join(PROJECT_DIR,'account/templates/'),
        os.path.join(PROJECT_DIR,'game/templates/'),
        os.path.join(PROJECT_DIR,'review/templates/'),
        os.path.join(PROJECT_DIR,'notification/templates/'),
        os.path.join(PROJECT_DIR, 'static/admin'),
        os.path.join(PROJECT_DIR, 'static/landing'),
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'account',
    'notification',
    'game',
    'court',
    'city',
    'review',
	'localflavor',
    'django_cleanup',
    'bootstrap3_datetime',
    'form_utils',
    'geoposition',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'TenniSoda.urls'

WSGI_APPLICATION = 'TenniSoda.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',

)
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'TenniSoda',
        'USER': 'root',
        'PASSWORD':'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = PROJECT_DIR

STATIC_URL = '/static/'

STATICFILES_DIRS=(
    ('assets', os.path.join(os.getcwd(),'static/')),        
)

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'static/')

MEDIA_URL = ''

UPLOAD_FILE_PATTERN = "uploaded_files/%s/%s_%s"

LOGGING = {
    'version':1,
    'disable_existing_loggers': True,
    'formatters':{
        'standard':{
            'format':'%(asctime)s [%(levelname)s] %(name)s: %(message)s'  
        },    
    },
    'handlers':{
        'default':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':'logs/mylog.log',
            'maxBytes':1024*1024*5,
            'backupCount':5,
            'formatter':'standard',
        },
        'request_handler':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':'logs/django_request.log',
            'maxBytes':1024*1024*5,
            'backupCount':5,
            'formatter':'standard',
        },
    },
    'loggers':{
        '':{
            'handlers':['default'],
            'level':'DEBUG',
            'propagate':True
        },
        'django.request':{
            'handlers':['request_handler'],
            'level':'DEBUG',
            'propagate':False,
        }, 
    }
}

AUTH_USER_MODEL = 'account.Account'

AUTH_PROFILE_MODULE = 'account.UserProfile'

#HOST_DOMAIN = 'ec2-54-191-12-220.us-west-2.compute.amazonaws.com'
HOST_DOMAIN = '127.0.0.1:8000'

