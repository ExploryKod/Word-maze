# Utilise l'image Docker officielle de Python (version plus récente)
FROM python:3.11-slim

WORKDIR /python-docker

# Installe les dépendances système et Node.js 22.x (compatible npm@11)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    ca-certificates \
    openssl && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Installe les dépendances Python
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Met à jour npm (npm@11 sera compatible avec Node 22)
RUN npm install -g npm@latest

# Crée le groupe et l'utilisateur www-data s'ils n'existent pas déjà
RUN (getent group www-data || groupadd -r www-data) && \
    (getent passwd www-data || useradd -r -g www-data www-data)

COPY . .
COPY app/package.json app/package-lock.json ./
RUN npm install
RUN npm install -g tailwindcss postcss autoprefixer

# Crée les répertoires nécessaires et définit les permissions pour www-data
RUN mkdir -p /python-docker/instance && \
    chown -R www-data:www-data /python-docker && \
    chmod 664 /python-docker/package-lock.json /python-docker/package.json && \
    chmod 755 /python-docker/instance && \
    chmod 755 /python-docker/app

# Copie le script d'initialisation et le rend exécutable
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh && \
    chown www-data:www-data /docker-entrypoint.sh

# Variables d'environnement
ARG ENV_CONTEXT=production
ENV ENVIRONMENT=$ENV_CONTEXT

# Change vers l'utilisateur non-root
USER www-data

# Expose le port
EXPOSE 5000

# Point d'entrée
ENTRYPOINT ["/docker-entrypoint.sh"]
