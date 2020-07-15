"""
Django settings for ultimate_frisbee_management project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import os

DEBUG = False
ALLOWED_HOSTS = ["159.69.181.225", "db-ultimate.frisbeeverband.at", "db-ultimate.oevsf.at","localhost"]

# Try reading the secret key from file. if not existent rewrite it.
secret_key_file = "/etc/credentials/django_secret_key.txt"
try:
    with open(secret_key_file) as f:
        SECRET_KEY = f.read().strip()

except FileNotFoundError:
    import random

    SECRET_KEY = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])
    os.makedirs(os.path.dirname(secret_key_file), exist_ok=True)
    with open(secret_key_file, "w+") as f:
        f.write(SECRET_KEY)

# Email settings
email_password_file = "/etc/credentials/email_pass.txt"
with open(email_password_file) as f:
    EMAIL_HOST_PASSWORD = f.read().strip()

EMAIL_HOST_USER = "db-ultimate@frisbeeverband.at"
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Datenbank Ultimate Österreich<db-ultimate@frisbeeverband.at>"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587

SERVER_EMAIL = "Datenbank Ultimate Error<db-ultimate@frisbeeverband.at>"
ADMIN = [("Florian Kain", "flokain11@gmail.com")]
