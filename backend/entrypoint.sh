python /var/www/html/backend/manage.py makemigrations
python /var/www/html/backend/manage.py migrate
python /var/www/html/backend/manage.py seed player_management
apache2ctl -D FOREGROUND