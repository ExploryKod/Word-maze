#!/bin/bash
# Script pour reconstruire l'image Docker sans cache et redémarrer le conteneur

echo "=== Arrêt des conteneurs ==="
docker-compose down

echo ""
echo "=== Suppression de l'ancienne image (optionnel) ==="
docker rmi word-maze 2>/dev/null || echo "Image non trouvée, pas de problème"

echo ""
echo "=== Reconstruction sans cache ==="
docker-compose build --no-cache

echo ""
echo "=== Démarrage des conteneurs ==="
docker-compose up -d

echo ""
echo "=== Vérification des logs ==="
docker-compose logs --tail=50 web

echo ""
echo "✅ Reconstruction terminée !"
echo ""
echo "Pour voir les logs en temps réel : docker-compose logs -f web"

