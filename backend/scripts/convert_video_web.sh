#!/bin/bash

# Script pour convertir la vidéo analysée en format compatible navigateur (H.264)

INPUT="results/queue_2_analysis/output_video.mp4"
OUTPUT="results/queue_2_analysis/output_video_web.mp4"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     🎬 Conversion Vidéo pour Compatibilité Navigateur         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Vérifier si ffmpeg est installé
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg n'est pas installé"
    echo "📦 Installation..."
    sudo apt-get update && sudo apt-get install -y ffmpeg
fi

echo "📹 Vidéo source: $INPUT"
echo "📹 Vidéo destination: $OUTPUT"
echo ""
echo "🔄 Conversion en cours (H.264 + AAC)..."
echo "   Cela peut prendre quelques minutes..."
echo ""

# Convertir avec H.264 (compatible navigateur)
ffmpeg -i "$INPUT" \
    -c:v libx264 \
    -preset fast \
    -crf 23 \
    -c:a aac \
    -b:a 128k \
    -movflags +faststart \
    -y \
    "$OUTPUT" 2>&1 | grep -E "(frame=|Duration:|size=|time=)" | tail -10

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Conversion réussie!"
    echo ""
    echo "📊 Informations:"
    ls -lh "$OUTPUT"
    echo ""
    echo "🎬 La vidéo compatible navigateur est disponible à:"
    echo "   $OUTPUT"
else
    echo ""
    echo "❌ Erreur lors de la conversion"
    exit 1
fi
