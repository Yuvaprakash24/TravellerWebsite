#!/bin/bash

# Install any dependencies (if necessary)
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput
