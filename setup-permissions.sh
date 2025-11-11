#!/bin/bash
# Script pour configurer les permissions locales pour package-lock.json

# Vérifie si le groupe www-data existe
if ! getent group www-data > /dev/null 2>&1; then
    echo "Création du groupe www-data..."
    sudo groupadd www-data
fi

# Ajoute l'utilisateur actuel au groupe www-data
echo "Ajout de l'utilisateur $USER au groupe www-data..."
sudo usermod -a -G www-data $USER

# Définit les permissions pour package-lock.json et package.json
if [ -f "package-lock.json" ]; then
    echo "Configuration des permissions pour package-lock.json..."
    sudo chown $USER:www-data package-lock.json
    sudo chmod 664 package-lock.json
fi

if [ -f "package.json" ]; then
    echo "Configuration des permissions pour package.json..."
    sudo chown $USER:www-data package.json
    sudo chmod 664 package.json
fi

echo ""
echo "✅ Permissions configurées !"
echo ""
echo "⚠️  Important : Pour que les changements de groupe prennent effet, vous devez :"
echo "   1. Vous déconnecter et vous reconnecter, OU"
echo "   2. Exécuter : newgrp www-data"
echo ""
echo "Ensuite, vous pourrez installer tarteaucitronjs avec : npm install tarteaucitronjs"

