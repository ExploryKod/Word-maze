#!/bin/bash
set -e

# Generate Flask secret key if not set
if [ -z "$SECRET_KEY" ]; then
    export SECRET_KEY=$(openssl rand -hex 32)
    echo "Generated SECRET_KEY: $SECRET_KEY" >&2
fi

# Set Flask app
export FLASK_APP=app:create_app

# Ensure Tailwind output directory exists
mkdir -p /python-docker/app/static/dist/css

# Start Tailwind CSS watcher in background (dev mode)
cd /python-docker/app
npx --yes tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch &
TAILWIND_PID=$!

# Wait a bit for initial compilation
sleep 2

# Return to root directory
cd /python-docker

# Start Flask development server with hot reloading
# Use custom Python script with stat-based reloader for Docker volume compatibility
echo "Starting Flask development server on port ${PORT:-5000} with hot reloading..."
export PYTHONUNBUFFERED=1
exec python /python-docker/run_dev.py

