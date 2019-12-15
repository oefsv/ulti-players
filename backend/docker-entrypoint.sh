#!/bin/sh
python manage.py makemigrations --no-input      
python manage.py migrate --no-input
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@admin.com', 'admin')" | python manage.py shell
gunicorn -c gunicorn_config.py ultimate_frisbee_management.wsgi