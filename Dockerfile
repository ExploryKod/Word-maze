#syntax=docker/dockerfile:1

# Utilise l'image Docker officielle de Python (version plus récente)
FROM python:3.11-slim

# Définit le répertoire de travail
WORKDIR /python-docker

# Installe les dépendances système et Node.js
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Installe les dépendances Python
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Met à jour npm
RUN npm install -g npm@latest
COPY . .
COPY app/package.json app/package-lock.json ./
RUN npm install
RUN npm install -g tailwindcss postcss autoprefixer

# Variables d'environnement - ne copie pas .env en production
# Les variables seront injectées par le gestionnaire Docker Hostinger
ARG ENV_CONTEXT=production
ENV ENVIRONMENT=$ENV_CONTEXT
# .env est exclu via .dockerignore pour la production

# Définit la commande par défaut pour lancer l'application
CMD ["bash", "-c", "if [ \"$ENVIRONMENT\" == \"production\" ]; then (cd app; npm run tailwind &) else (cd app; npm run tailwind-dev &) fi && gunicorn -w 4 -b 0.0.0.0:${PORT:-5000} 'app:create_app()'"]



