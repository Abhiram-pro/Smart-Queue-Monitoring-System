#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     🚀 Lancement du Dashboard Queue Monitoring System         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if server is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Un serveur est déjà en cours d'exécution sur le port 8000"
    echo ""
    read -p "Voulez-vous le tuer et redémarrer? (o/N): " choice
    if [[ "$choice" =~ ^[oOyY]$ ]]; then
        echo "🔄 Arrêt du serveur existant..."
        lsof -ti:8000 | xargs kill -9 2>/dev/null
        sleep 1
    else
        echo "✅ Ouverture du dashboard existant..."
        xdg-open "http://localhost:8000/dashboard_clean.html" 2>/dev/null || \
        firefox "http://localhost:8000/dashboard_clean.html" &
        exit 0
    fi
fi

echo "🔧 Démarrage du serveur HTTP..."
python3 start_dashboard.py &
SERVER_PID=$!

sleep 2

echo "✅ Serveur démarré (PID: $SERVER_PID)"
echo "🌐 URL: http://localhost:8000/dashboard_clean.html"
echo ""
echo "📊 Le dashboard affiche maintenant les DONNÉES RÉELLES de:"
echo "   • results/queue_2_analysis/queue_statistics.csv"
echo ""
echo "💡 Appuyez sur Ctrl+C pour arrêter le serveur"
echo "════════════════════════════════════════════════════════════════"

# Keep script running
wait $SERVER_PID
