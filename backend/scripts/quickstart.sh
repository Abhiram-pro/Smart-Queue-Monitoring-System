#!/bin/bash

# Queue Analytics System - Quick Start Script
# This script helps you get started quickly

echo "======================================================================"
echo "🎯 QUEUE ANALYTICS SYSTEM - QUICK START"
echo "======================================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 detected: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "======================================================================"
echo "✅ SETUP COMPLETE!"
echo "======================================================================"
echo ""
echo "Choose how to start:"
echo ""
echo "1️⃣  START DASHBOARD (Recommended)"
echo "   Run: python3 dashboard_server.py"
echo "   Then open: http://localhost:5000"
echo ""
echo "2️⃣  ANALYZE VIDEO DIRECTLY"
echo "   Run: python3 queue_analyzer.py test/queue_1.mp4"
echo ""
echo "3️⃣  DRAW ZONES ONLY"
echo "   Run: python3 draw_zones.py test/queue_1.mp4"
echo ""
echo "4️⃣  RESIZE LARGE VIDEO"
echo "   Run: python3 resize_video.py input.mp4 output.mp4 0.5"
echo ""
echo "======================================================================"
echo "📖 For detailed documentation, see DASHBOARD_README.md"
echo "======================================================================"
echo ""

# Ask user what to do
read -p "Would you like to start the dashboard now? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Starting dashboard server..."
    echo ""
    python3 dashboard_server.py
fi
