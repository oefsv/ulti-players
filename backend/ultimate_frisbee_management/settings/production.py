"""
Django settings for ultimate_frisbee_management project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

# Try reading the secret key from file. if not existent rewrite it.
try:
    with open('/etc/credentials/django_secret_key.txt') as f:
        SECRET_KEY = f.read().strip()

except FileNotFoundError as e:
    import random
    
    SECRET_KEY = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])
    
    with open('/etc/credentials/django_secret_key.txt',"w+") as f:
        f.write(SECRET_KEY)
    

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db', # set in docker-compose.yml
        'PORT': 5432 # default postgres port
    }
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ""
EMAIL_PORT = 2587
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Admin<admin@domain.com>" 