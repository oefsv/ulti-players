# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# WORKS:
# EMAIL_HOST_USER = "florian.c.kain@gmail.com"
# EMAIL_HOST_PASSWORD = "flomaster88"
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = "Dev Admin<dev.datenbank@frisbeeverband.at>" 
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/workspace/backend/ultimate_frisbee_management/tests/mails' # change this to a proper location