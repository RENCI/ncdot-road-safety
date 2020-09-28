#!/bin/bash
# Collect static files to be served

echo "yes" | docker exec -i dot-server python manage.py collectstatic