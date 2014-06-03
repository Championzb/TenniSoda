"""
Django settings for TenniSoda project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

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
	'localflavor',
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

MEDIA_ROOT = os.path.join(PROJECT_DIR,'static/')

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
