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

COPY . .
COPY app/package.json app/package-lock.json ./
RUN npm install
RUN npm install -g tailwindcss postcss autoprefixer

# Copie le script d'initialisation et le rend exécutable
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Variables d'environnement
ARG ENV_CONTEXT=production
ENV ENVIRONMENT=$ENV_CONTEXT

# Expose le port
EXPOSE 5000

# Point d'entrée
ENTRYPOINT ["/docker-entrypoint.sh"]
