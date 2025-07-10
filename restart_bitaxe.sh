#!/bin/bash

# Liste des adresses IP des serveurs Bitaxe
BITAXE_IPS=(
    "192.168.1.19"
    "192.168.1.51"
    # Ajoutez d'autres IP ici
)

# Fonction pour redémarrer un serveur
restart_bitaxe() {
    local ip=$1
    echo "Redémarrage de Bitaxe à l'adresse $ip..."
    response=$(curl -s -X POST "http://$ip/api/system/restart" -w "\nHTTP_STATUS:%{http_code}")
    
    # Extraction du code HTTP
    http_status=$(echo "$response" | grep HTTP_STATUS | cut -d':' -f2)
    
    if [ "$http_status" -eq 200 ]; then
        echo "Redémarrage réussi pour $ip"
    else
        echo "Erreur lors du redémarrage de $ip (Code HTTP: $http_status)"
    fi
}

# Vérification si la liste contient des IPs
if [ ${#BITAXE_IPS[@]} -eq 0 ]; then
    echo "Erreur : Aucune adresse IP configurée dans BITAXE_IPS"
    exit 1
fi

# Boucle sur chaque IP pour lancer le redémarrage
for ip in "${BITAXE_IPS[@]}"; do
    restart_bitaxe "$ip"
    # Pause de 2 secondes entre chaque redémarrage
    sleep 2
done

echo "Opération terminée"
