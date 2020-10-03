#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

for pc in $(seq 3 -1 1); do
    echo -ne "$pc ...\033[0K\r"
    sleep 1
done

psql -h db -f pg.production.sql --quiet
python manage.py collectstatic --no-input --clear
python manage.py migrate sites --noinput
python manage.py migrate --no-input

exec "$@"
