#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Crear superusuario
echo "from django.contrib.auth.models import User; User.objects.create_superuser('Adminuser', 'juan.romero.c@uniminuto.edu', 'Holamundo456')" | python manage.py shell
