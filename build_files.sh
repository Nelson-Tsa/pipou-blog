#!/bin/bash

# Build the project
echo "Building the project..."

# Install dependencies
pip3 install -r requirements.txt

# Navigate to Django project directory
cd pipou_blog

# Set environment variables for build
export DJANGO_SETTINGS_MODULE=pipou_blog.settings
export DEBUG=False

# Use a dummy DATABASE_URL if not set (for collectstatic only)
if [ -z "$DATABASE_URL" ]; then
    export DATABASE_URL="sqlite:///dummy.db"
fi

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

# Move staticfiles to root for Vercel
echo "Moving static files to root..."
cd ..
cp -r pipou_blog/staticfiles ./staticfiles

echo "Build completed successfully!"
