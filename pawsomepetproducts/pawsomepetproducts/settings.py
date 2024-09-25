"""
Django settings for pawsomepetproducts project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)


ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    #thirdparty
    'bootstrap5',
    'crispy_forms',
    'crispy_bootstrap5',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'active_link', #addedto make menu links active when it is selected
    'whitenoise.runserver_nostatic', # for collecting static files
    
    #local
    'user_home',
    'accounts',
    'customadmin',
    'category',
    'pet_type',
    'product',
    'cart',
    'orders',
    'wishlist',
    'coupons',
    'wallet',
    'offers',
]


#for adding django crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # added to collect static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', # for social authentication
    'accounts.middleware.BlockUserMiddleware', #custom middleware added to logout user after he is blocked
    
]

ROOT_URLCONF = 'pawsomepetproducts.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.counter', #added to get the number of items in the cart in all pages except admin
                'wishlist.context_processors.wishlist_counter' #added to get the mumber of items in wishlist of a authenticated user
               
            ],
        },
    },
]


#added to  integrate django social authentication
AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
    
]


WSGI_APPLICATION = 'pawsomepetproducts.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),  
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata' #changed timezone to ITC

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    ]
STATIC_ROOT = "/var/www/pawsomepetproducts/static/"


#Media files configuration

# Base url to serve media files
MEDIA_URL = '/media/'
# Path where media is stored'
MEDIA_ROOT = BASE_DIR / 'media'




# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#Setting CustomUserModel as authorised model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Provider specific settings for social authentication
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
                'profile',
                'email',
        ],
        'AUTH_PARAMS': {
            'access_type' : 'online',
        }
        
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
    #     'APP': {
    #         'client_id': '123',
    #         'secret': '456',
    #         'key': ''
    #     }
    }
}



ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'



ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


#Configuration for sending emails
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

#Razor Pay API keys
RAZOR_KEY_ID = config('RAZOR_KEY_ID')
RAZOR_KEY_SECRET = config('RAZOR_KEY_SECRET')

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

#Twilio Integration
ACCOUNT_SID=config('ACCOUNT_SID')
AUTH_TOKEN=config('AUTH_TOKEN')
TWILIO_PHONE_NUMBER=config('TWILIO_PHONE_NUMBER')