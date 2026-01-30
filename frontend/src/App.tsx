import { useState, useEffect } from 'react';
import { io, Socket } from 'socket.io-client';
import ZoneDrawer from './ZoneDrawer';
import './App.css';

interface Customer {
  id: number;
  zone: string;
  waitTime: number;
  status: string;
  hasAlert: boolean;
}

interface Stats {
  totalPeople: number;
  inQueue: number;
  atCashdesk: number;
  completed: number;
  avgWaitTime: number;
  maxWaitTime: number;
  alerts: number;
}

interface QueueData {
  frame: number;
  timestamp: string;
  stats: Stats;
  customers: Customer[];
  videoFrame: string;
}

interface Zone {
  name: string;
  polygon: Array<{ x: number; y: number }>;
}

function App() {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [connected, setConnected] = useState(false);
  const [cameraActive, setCameraActive] = useState(false);
  const [data, setData] = useState<QueueData | null>(null);
  const [showZoneDrawer, setShowZoneDrawer] = useState(false);
  const [capturedFrame, setCapturedFrame] = useState<string | null>(null);
  const [zonesConfigured, setZonesConfigured] = useState(false);

  useEffect(() => {
    const wsUrl = process.env.REACT_APP_WS_URL || 'http://localhost:5001';
    const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5001';
    
    console.log('Connecting to:', wsUrl);
    const newSocket = io(wsUrl, {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    });
    
    newSocket.on('connect', () => {
      console.log('✅ Connected to WebSocket server');
      setConnected(true);
      
      // Check if zones are configured
      fetch(`${apiUrl}/api/status`)
        .then(res => {
          if (!res.ok) throw new Error('Failed to fetch status');
          return res.json();
        })
        .then(data => {
          setZonesConfigured(data.zones_configured);
        })
        .catch(err => {
          console.error('Failed to check status:', err);
          // Don't show alert on initial load, just log
        });
    });

    newSocket.on('disconnect', () => {
      console.log('❌ Disconnected from server');
      setConnected(false);
    });

    newSocket.on('queue_update', (updateData: QueueData) => {
      setData(updateData);
    });

    newSocket.on('camera_started', () => {
      setCameraActive(true);
    });

    newSocket.on('camera_stopped', () => {
      setCameraActive(false);
    });

    newSocket.on('error', (error: { message: string }) => {
      console.error('Server error:', error.message);
      // Only alert for critical errors, not connection issues
      if (!error.message.includes('connect') && !error.message.includes('timeout')) {
        alert(`Error: ${error.message}`);
      }
    });

    newSocket.on('frame_captured', (frameData: { frame: string }) => {
      setCapturedFrame(frameData.frame);
      setShowZoneDrawer(true);
    });

    newSocket.on('zones_saved', (response: { status: string; message: string }) => {
      console.log('Zones saved:', response.message);
      setZonesConfigured(true);
      alert('✅ Zones saved successfully!');
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  const startCamera = () => {
    if (socket) {
      socket.emit('start_camera', { camera_id: 0, confidence: 0.45 });
    }
  };

  const stopCamera = () => {
    if (socket) {
      socket.emit('stop_camera');
    }
  };

  const captureFrameForZones = () => {
    if (socket) {
      socket.emit('capture_frame');
    }
  };

  const handleZonesSaved = (zones: Zone[]) => {
    if (socket) {
      // Convert zones to the format expected by the server
      const zonesConfig = {
        zones: zones.map(zone => ({
          name: zone.name,
          polygon: zone.polygon.map(p => [p.x, p.y])
        }))
      };
      
      socket.emit('save_zones', zonesConfig);
      setShowZoneDrawer(false);
      setCapturedFrame(null);
    }
  };

  const handleZoneDrawerCancel = () => {
    setShowZoneDrawer(false);
    setCapturedFrame(null);
  };

  return (
    <div className="App">
      <header className="header">
        <h1>🎯 Smart Queue Monitoring System</h1>
        <div className="connection-status">
          <span className={connected ? 'status-dot connected' : 'status-dot'} />
          {connected ? 'Connected' : 'Disconnected'}
        </div>
      </header>

      <div className="controls">
        <button 
          onClick={captureFrameForZones} 
          disabled={!connected || cameraActive}
          className="btn btn-zones"
        >
          🎨 Configure Zones
        </button>
        <button 
          onClick={startCamera} 
          disabled={!connected || cameraActive || !zonesConfigured}
          className="btn btn-start"
          title={!zonesConfigured ? 'Configure zones first' : ''}
        >
          {cameraActive ? '🎥 Camera Running' : '▶️ Start Camera'}
        </button>
        <button 
          onClick={stopCamera} 
          disabled={!connected || !cameraActive}
          className="btn btn-stop"
        >
          ⏹️ Stop Camera
        </button>
      </div>

      {!zonesConfigured && (
        <div className="warning-banner">
          ⚠️ No zones configured. Click "Configure Zones" to set up detection areas.
        </div>
      )}

      {data && (
        <>
          <div className="stats-grid">
            <div className="stat-card queue">
              <div className="stat-icon">👥</div>
              <div className="stat-value">{data.stats.inQueue}</div>
              <div className="stat-label">En Queue</div>
            </div>
            <div className="stat-card cashdesk">
              <div className="stat-icon">💳</div>
              <div className="stat-value">{data.stats.atCashdesk}</div>
              <div className="stat-label">À la Caisse</div>
            </div>
            <div className="stat-card wait-time">
              <div className="stat-icon">⏱️</div>
              <div className="stat-value">{data.stats.avgWaitTime}s</div>
              <div className="stat-label">Temps d'Attente Moyen</div>
            </div>
            <div className="stat-card total">
              <div className="stat-icon">📊</div>
              <div className="stat-value">{data.stats.totalPeople}</div>
              <div className="stat-label">Total Détecté</div>
            </div>
          </div>

          <div className="content-grid">
            <div className="video-section">
              <h2>📹 Live Feed</h2>
              {data.videoFrame && (
                <img 
                  src={`data:image/jpeg;base64,${data.videoFrame}`} 
                  alt="Live camera feed"
                  className="video-frame"
                />
              )}
              <div className="video-info">
                Frame: {data.frame} | {new Date(data.timestamp).toLocaleTimeString()}
              </div>
            </div>

            <div className="customers-section">
              <h2>👤 Customers ({data.customers.length})</h2>
              <div className="customers-table">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Zone</th>
                      <th>Wait Time</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.customers.length === 0 ? (
                      <tr>
                        <td colSpan={4} className="no-data">No customers detected</td>
                      </tr>
                    ) : (
                      data.customers.map((customer) => (
                        <tr key={customer.id} className={customer.hasAlert ? 'alert-row' : ''}>
                          <td>#{customer.id}</td>
                          <td>
                            <span className={`zone-badge ${customer.zone.toLowerCase().replace(' ', '-')}`}>
                              {customer.zone}
                            </span>
                          </td>
                          <td>{customer.waitTime}s</td>
                          <td>
                            <span className={`status-badge ${customer.status}`}>
                              {customer.status === 'alert' ? '⚠️ Alert' : 
                               customer.status === 'waiting' ? '⏳ Waiting' : '✅ Serving'}
                            </span>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div className="summary-section">
            <div className="summary-item">
              <strong>Max Wait Time:</strong> {data.stats.maxWaitTime}s
            </div>
            <div className="summary-item">
              <strong>Completed:</strong> {data.stats.completed}
            </div>
            <div className="summary-item">
              <strong>Alerts:</strong> {data.stats.alerts}
            </div>
          </div>
        </>
      )}

      {!data && cameraActive && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Waiting for camera data...</p>
        </div>
      )}

      {!cameraActive && !data && (
        <div className="welcome">
          <h2>👋 Welcome to Smart Queue Monitoring</h2>
          <p>
            {zonesConfigured 
              ? 'Click "Start Camera" to begin real-time monitoring'
              : 'Click "Configure Zones" to set up detection areas first'}
          </p>
        </div>
      )}

      {showZoneDrawer && capturedFrame && (
        <ZoneDrawer
          videoFrame={capturedFrame}
          onZonesSaved={handleZonesSaved}
          onCancel={handleZoneDrawerCancel}
        />
      )}
    </div>
  );
}

export default App;
