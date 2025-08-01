#!/bin/bash

# Build the project
echo "Building the project..."

# Install dependencies
pip3 install -r requirements.txt

# Collect static files
cd pipou_blog
python3 manage.py collectstatic --noinput --clear
