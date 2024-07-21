#!/bin/sh
echo "Running collectstatic..."
python manage.py collectstatic --noinput
echo "Collectstatic completed."
