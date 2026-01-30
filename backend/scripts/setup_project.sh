#!/bin/bash

echo "🎯 Setting up Smart Queue Monitoring System..."
echo "================================================"

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p src
mkdir -p data/test
mkdir -p data/results
mkdir -p scripts
mkdir -p config
mkdir -p docs

# Move Python source files
echo "📦 Organizing source files..."
mv queue_analyzer.py src/ 2>/dev/null || true
mv person_detect.py src/ 2>/dev/null || true
mv draw_zones.py src/ 2>/dev/null || true
mv live_viewer.py src/ 2>/dev/null || true
mv api_server.py src/ 2>/dev/null || true

# Move utility scripts
mv generate_clean_data.py scripts/ 2>/dev/null || true
mv generate_realistic_data.py scripts/ 2>/dev/null || true
mv analyze_queue_counts.py scripts/ 2>/dev/null || true
mv create_sample_queue_param.py scripts/ 2>/dev/null || true
mv extract_frames.py scripts/ 2>/dev/null || true
mv resize_video.py scripts/ 2>/dev/null || true
mv verify_chart_data.py scripts/ 2>/dev/null || true

# Move test scripts
mv test_*.py scripts/ 2>/dev/null || true

# Move dashboard files
mv dashboard*.html src/ 2>/dev/null || true
mv start_dashboard.py src/ 2>/dev/null || true

# Move config files
mv zones*.json config/ 2>/dev/null || true

# Move shell scripts
mv *.sh scripts/ 2>/dev/null || true

# Move code.py if exists
mv code.py src/ 2>/dev/null || true

# Keep requirements.txt and README.md in root
echo "✅ File organization complete!"

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -q ultralytics opencv-python numpy supervision flask flask-cors flask-socketio python-socketio inference

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Project Structure:"
echo "├── src/              # Source code"
echo "├── scripts/          # Utility scripts"
echo "├── data/             # Data files"
echo "│   ├── test/         # Test videos"
echo "│   └── results/      # Analysis results"
echo "├── config/           # Configuration files"
echo "└── docs/             # Documentation"
echo ""
echo "🚀 Ready to run!"
