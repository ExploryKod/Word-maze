#syntax=docker/dockerfile:1

# Utilise l'image Docker officielle de Python 3.8
FROM python:3.8-slim-buster

# Définit le répertoire de travail
WORKDIR /python-docker

# Installe les dépendances Python
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Installe Node.js et les dépendances pour l'application front-end
RUN apt-get update && apt-get install -y curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
RUN npm install --update npm
COPY . .
COPY app/package.json app/package-lock.json ./
RUN npm install
RUN npm install -g tailwindcss postcss autoprefixer


# Définit la commande par défaut pour lancer l'application
CMD ["bash", "-c", "(cd app; npm run tailwind &) && gunicorn -w 4 -b 0.0.0.0:${PORT:-5000} 'app:create_app()'"]



