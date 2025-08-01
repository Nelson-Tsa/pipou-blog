#!/bin/bash

# Build the project
echo "Building the project..."

# Install dependencies
pip3 install -r requirements.txt

# Collect static files
cd pipou_blog

# Set a dummy DATABASE_URL for collectstatic if not set
export DATABASE_URL=${DATABASE_URL:-"postgresql://dummy:dummy@dummy:5432/dummy"}

python3 manage.py collectstatic --noinput --clear
