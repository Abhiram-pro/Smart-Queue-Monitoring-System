"""
Smart Queue Monitoring System - Backend Server
Flask API + WebSocket server for real-time queue monitoring
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
import threading

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Get port from environment variable (Railway sets this)
PORT = int(os.environ.get('PORT', 5000))

# Load configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config', 'zones.json')

# Import queue monitor
try:
    from queue_monitor import QueueMonitor
    monitor = QueueMonitor(socketio, CONFIG_PATH)
    MONITOR_AVAILABLE = True
    print("✅ Queue monitor loaded")
except Exception as e:
    print(f"⚠️ Queue monitor not available: {e}")
    print("   Install requirements: pip install ultralytics opencv-python")
    MONITOR_AVAILABLE = False
    monitor = None

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'service': 'Smart Queue Monitoring System',
        'version': '1.0.0'
    })

@app.route('/api/health')
def health():
    """Health check for monitoring"""
    return jsonify({'status': 'healthy'})

@app.route('/api/status')
def get_status():
    """Get system status"""
    try:
        zones_configured = False
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
                zones_configured = len(config.get('zones', [])) > 0
        
        return jsonify({
            'status': 'running',
            'zones_configured': zones_configured,
            'camera_active': False
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config')
def get_config():
    """Get zone configuration"""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
            return jsonify(config)
        else:
            return jsonify({'zones': []})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print('Client connected')
    emit('connection_response', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected')

@socketio.on('queue_update')
def handle_queue_update(data):
    """Handle queue update from monitoring system"""
    # Broadcast to all connected clients
    emit('queue_data', data, broadcast=True)

@socketio.on('request_data')
def handle_data_request():
    """Handle data request from client"""
    # Send mock data for now
    emit('queue_data', {
        'timestamp': '2024-01-30T18:00:00',
        'zones': [
            {'id': 1, 'name': 'Zone 1', 'count': 5, 'status': 'normal'},
            {'id': 2, 'name': 'Zone 2', 'count': 12, 'status': 'warning'}
        ]
    })

@socketio.on('start_camera')
def handle_start_camera(data):
    """Handle camera start request"""
    print(f'Camera start requested: {data}')
    
    if not MONITOR_AVAILABLE:
        emit('error', {'message': 'AI monitoring not available. Install: pip install ultralytics opencv-python'})
        return
    
    if monitor.running:
        emit('error', {'message': 'Camera already running'})
        return
    
    # Start monitoring in background thread
    monitor_thread = threading.Thread(target=monitor.run)
    monitor_thread.daemon = True
    monitor_thread.start()

@socketio.on('stop_camera')
def handle_stop_camera():
    """Handle camera stop request"""
    print('Camera stop requested')
    
    if not MONITOR_AVAILABLE:
        return
    
    if monitor.running:
        monitor.stop()

@socketio.on('capture_frame')
def handle_capture_frame():
    """Handle frame capture for zone configuration"""
    print('Frame capture requested')
    
    if not MONITOR_AVAILABLE:
        emit('error', {'message': 'Camera not available'})
        return
    
    # Capture frame
    frame_base64 = monitor.capture_frame_for_zones()
    
    if frame_base64:
        emit('frame_captured', {'frame': frame_base64})
    else:
        emit('error', {'message': 'Failed to capture frame'})

@socketio.on('save_zones')
def handle_save_zones(data):
    """Handle zone configuration save"""
    print(f'Zones save requested: {data}')
    try:
        # Save zones to config file
        with open(CONFIG_PATH, 'w') as f:
            json.dump(data, f, indent=2)
        emit('zones_saved', {'status': 'success', 'message': 'Zones saved successfully'})
    except Exception as e:
        emit('error', {'message': f'Failed to save zones: {str(e)}'})

if __name__ == '__main__':
    print(f'🚀 Starting server on port {PORT}')
    print(f'📡 WebSocket enabled')
    print(f'🌐 CORS enabled for all origins')
    socketio.run(app, host='0.0.0.0', port=PORT, debug=False)
