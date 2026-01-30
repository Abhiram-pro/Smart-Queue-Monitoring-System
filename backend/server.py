"""
Smart Queue Monitoring System - Backend Server
Flask API + WebSocket server for real-time queue monitoring
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Get port from environment variable (Railway sets this)
PORT = int(os.environ.get('PORT', 5000))

# Load configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config', 'zones.json')

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

if __name__ == '__main__':
    print(f'🚀 Starting server on port {PORT}')
    print(f'📡 WebSocket enabled')
    print(f'🌐 CORS enabled for all origins')
    socketio.run(app, host='0.0.0.0', port=PORT, debug=False)
