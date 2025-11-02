#!/bin/bash
set -e

# Génère une clé secrète Flask si elle n'est pas définie
if [ -z "$SECRET_KEY" ]; then
    export SECRET_KEY=$(openssl rand -hex 32)
    echo "Generated SECRET_KEY: $SECRET_KEY" >&2
fi

# Compile Tailwind CSS en production
if [ "$ENVIRONMENT" == "production" ]; then
    cd app && npm run tailwind &
else
    cd app && npm run tailwind-dev &
fi

# Attendre un peu pour que Tailwind compile
sleep 2

# Retour au répertoire racine
cd /python-docker

# Démarre Gunicorn
exec gunicorn -w 4 -b 0.0.0.0:${PORT:-5000} 'app:create_app()'

