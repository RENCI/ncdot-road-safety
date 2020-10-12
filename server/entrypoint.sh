#!/bin/bash
set -e 

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

if [ -v PGPASSWORD ]; then
  for pc in $(seq 3 -1 1); do
    echo -ne "$pc ...\033[0K\r"
    sleep 1
  done

  psql -U postgres -h db -f pg.develop.sql --quiet
  #export DJANGO_SUPERUSER_PASSWORD="fill_in_password"
  python manage.py collectstatic --no-input --clear
  #python manage.py makemigrations rs_core --noinput
  python manage.py migrate sites --noinput
  python manage.py migrate --no-input
  #python manage.py createsuperuser --username admin --email admin@example.com --no-input
fi

exec "$@"
