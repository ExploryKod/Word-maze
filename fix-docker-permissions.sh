#!/bin/bash
# Script pour corriger les permissions Docker sur le VPS

echo "=== Correction des permissions Docker ==="

# Vérifier si le groupe docker existe
if ! getent group docker > /dev/null 2>&1; then
    echo "Création du groupe docker..."
    sudo groupadd docker
fi

# Ajouter l'utilisateur actuel au groupe docker
echo "Ajout de l'utilisateur $USER au groupe docker..."
sudo usermod -aG docker $USER

# Corriger les permissions du socket Docker
echo "Correction des permissions du socket Docker..."
sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock

# Vérifier les permissions
echo ""
echo "=== Vérification ==="
ls -l /var/run/docker.sock
echo ""
echo "Groupes de l'utilisateur $USER :"
groups $USER

echo ""
echo "✅ Permissions corrigées !"
echo ""
echo "⚠️  IMPORTANT : Pour que les changements prennent effet :"
echo "   1. Déconnectez-vous et reconnectez-vous, OU"
echo "   2. Exécutez : newgrp docker"
echo ""
echo "Ensuite, testez avec : docker ps"

