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
    export DATABASE_URL="postgresql://dummy:dummy@dummy:5432/dummy"
fi

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

# Create staticfiles_build directory structure for Vercel
echo "Creating staticfiles_build structure..."
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/

echo "Build completed successfully!"
