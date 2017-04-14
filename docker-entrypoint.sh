#!/bin/sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Create superuser if does not exist
echo "Create superuser if does not exist"
script="
from django.contrib.auth.models import User;

username = '$SUPERUSER';
password = '$SUPERUSER_PASS';
email = '$SUPERUSER_MAIL';

if User.objects.filter(username=username).count()==0:
    User.objects.create_superuser(username, email, password);
    print('Superuser created.');
else:
    print('Superuser creation skipped.');
"
printf "$script" | python manage.py shell

# Start server
echo "Starting server"
echo "Superuser is $SUPERUSER"
gunicorn ac_rank.wsgi:application --bind :9001 --workers=2
