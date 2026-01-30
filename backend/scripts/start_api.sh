#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        🚀 Lancement du Serveur API Flask                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Kill any existing process on port 5000
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Un serveur tourne déjà sur le port 5000"
    read -p "Voulez-vous le tuer et redémarrer? (o/N): " choice
    if [[ "$choice" =~ ^[oOyY]$ ]]; then
        echo "🔄 Arrêt du serveur existant..."
        lsof -ti:5000 | xargs kill -9 2>/dev/null
        sleep 1
    else
        echo "✅ Serveur existant maintenu"
        exit 0
    fi
fi

echo "🔧 Vérification des dépendances..."
python3 -c "import flask, flask_cors, flask_socketio" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dépendances manquantes"
    echo "📦 Installation..."
    pip3 install flask flask-cors flask-socketio python-socketio
fi

echo ""
echo "🚀 Démarrage du serveur API..."
echo "═══════════════════════════════════════════════════════════════"
echo ""

python3 api_server.py
