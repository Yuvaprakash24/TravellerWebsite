#!/bin/bash
echo "Check check....."
# Install any dependencies (if necessary)
pip3 install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput
