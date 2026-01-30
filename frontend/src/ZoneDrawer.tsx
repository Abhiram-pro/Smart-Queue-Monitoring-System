import { useState, useRef, useEffect } from 'react';
import './ZoneDrawer.css';

interface Point {
  x: number;
  y: number;
}

interface Zone {
  name: string;
  polygon: Point[];
}

interface ZoneDrawerProps {
  videoFrame: string | null;
  onZonesSaved: (zones: Zone[]) => void;
  onCancel: () => void;
}

function ZoneDrawer({ videoFrame, onZonesSaved, onCancel }: ZoneDrawerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [zones, setZones] = useState<Zone[]>([]);
  const [currentZone, setCurrentZone] = useState<Point[]>([]);
  const [currentZoneName, setCurrentZoneName] = useState('Queue Line');
  const [imageLoaded, setImageLoaded] = useState(false);
  const imageRef = useRef<HTMLImageElement | null>(null);

  const zoneNames = ['Queue Line', 'Cash Desk', 'Completed', 'Worker Area'];
  const zoneColors = ['#fbbf24', '#ef4444', '#10b981', '#6b7280'];

  useEffect(() => {
    if (videoFrame) {
      const img = new Image();
      img.onload = () => {
        imageRef.current = img;
        setImageLoaded(true);
        drawCanvas();
      };
      img.src = `data:image/jpeg;base64,${videoFrame}`;
    }
  }, [videoFrame]);

  useEffect(() => {
    if (imageLoaded) {
      drawCanvas();
    }
  }, [currentZone, zones, imageLoaded]);

  const drawCanvas = () => {
    const canvas = canvasRef.current;
    const img = imageRef.current;
    if (!canvas || !img) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size to match image
    canvas.width = img.width;
    canvas.height = img.height;

    // Draw image
    ctx.drawImage(img, 0, 0);

    // Draw completed zones
    zones.forEach((zone, idx) => {
      if (zone.polygon.length > 0) {
        ctx.fillStyle = zoneColors[idx % zoneColors.length] + '40';
        ctx.strokeStyle = zoneColors[idx % zoneColors.length];
        ctx.lineWidth = 3;

        ctx.beginPath();
        ctx.moveTo(zone.polygon[0].x, zone.polygon[0].y);
        zone.polygon.forEach(point => {
          ctx.lineTo(point.x, point.y);
        });
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        // Draw zone name
        const centerX = zone.polygon.reduce((sum, p) => sum + p.x, 0) / zone.polygon.length;
        const centerY = zone.polygon.reduce((sum, p) => sum + p.y, 0) / zone.polygon.length;
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 20px Arial';
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 3;
        ctx.strokeText(zone.name, centerX - 50, centerY);
        ctx.fillText(zone.name, centerX - 50, centerY);

        // Draw points
        zone.polygon.forEach(point => {
          ctx.fillStyle = zoneColors[idx % zoneColors.length];
          ctx.beginPath();
          ctx.arc(point.x, point.y, 6, 0, 2 * Math.PI);
          ctx.fill();
        });
      }
    });

    // Draw current zone being drawn
    if (currentZone.length > 0) {
      const currentIdx = zones.length;
      ctx.fillStyle = zoneColors[currentIdx % zoneColors.length] + '40';
      ctx.strokeStyle = zoneColors[currentIdx % zoneColors.length];
      ctx.lineWidth = 3;

      if (currentZone.length > 2) {
        ctx.beginPath();
        ctx.moveTo(currentZone[0].x, currentZone[0].y);
        currentZone.forEach(point => {
          ctx.lineTo(point.x, point.y);
        });
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
      } else if (currentZone.length === 2) {
        ctx.beginPath();
        ctx.moveTo(currentZone[0].x, currentZone[0].y);
        ctx.lineTo(currentZone[1].x, currentZone[1].y);
        ctx.stroke();
      }

      // Draw points
      currentZone.forEach((point, idx) => {
        ctx.fillStyle = zoneColors[currentIdx % zoneColors.length];
        ctx.beginPath();
        ctx.arc(point.x, point.y, 6, 0, 2 * Math.PI);
        ctx.fill();
        
        // Draw point number
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 14px Arial';
        ctx.fillText(`${idx + 1}`, point.x - 5, point.y - 10);
      });
    }
  };

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;

    setCurrentZone([...currentZone, { x, y }]);
  };

  const handleCanvasRightClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    if (currentZone.length >= 3) {
      completeZone();
    }
  };

  const completeZone = () => {
    if (currentZone.length >= 3) {
      setZones([...zones, { name: currentZoneName, polygon: currentZone }]);
      setCurrentZone([]);
      
      // Auto-select next zone name
      const nextIdx = zones.length + 1;
      if (nextIdx < zoneNames.length) {
        setCurrentZoneName(zoneNames[nextIdx]);
      }
    }
  };

  const undoLastPoint = () => {
    if (currentZone.length > 0) {
      setCurrentZone(currentZone.slice(0, -1));
    }
  };

  const clearCurrentZone = () => {
    setCurrentZone([]);
  };

  const deleteZone = (idx: number) => {
    setZones(zones.filter((_, i) => i !== idx));
  };

  const handleSave = () => {
    if (zones.length === 0) {
      alert('Please draw at least one zone before saving!');
      return;
    }
    onZonesSaved(zones);
  };

  return (
    <div className="zone-drawer-overlay">
      <div className="zone-drawer-container">
        <div className="zone-drawer-header">
          <h2>🎨 Draw Detection Zones</h2>
          <button onClick={onCancel} className="close-btn">✕</button>
        </div>

        <div className="zone-drawer-content">
          <div className="canvas-container">
            <canvas
              ref={canvasRef}
              onClick={handleCanvasClick}
              onContextMenu={handleCanvasRightClick}
              className="drawing-canvas"
            />
          </div>

          <div className="zone-drawer-controls">
            <div className="control-section">
              <h3>Current Zone</h3>
              <select 
                value={currentZoneName} 
                onChange={(e) => setCurrentZoneName(e.target.value)}
                disabled={currentZone.length > 0}
              >
                {zoneNames.map(name => (
                  <option key={name} value={name}>{name}</option>
                ))}
              </select>
              <div className="zone-info">
                Points: {currentZone.length}
                {currentZone.length >= 3 && (
                  <span className="ready-indicator">✓ Ready to complete</span>
                )}
              </div>
            </div>

            <div className="control-section">
              <h3>Actions</h3>
              <button onClick={undoLastPoint} disabled={currentZone.length === 0}>
                ↶ Undo Point
              </button>
              <button onClick={clearCurrentZone} disabled={currentZone.length === 0}>
                🗑️ Clear Zone
              </button>
              <button 
                onClick={completeZone} 
                disabled={currentZone.length < 3}
                className="btn-complete"
              >
                ✓ Complete Zone
              </button>
            </div>

            <div className="control-section">
              <h3>Completed Zones ({zones.length})</h3>
              <div className="zones-list">
                {zones.length === 0 ? (
                  <p className="no-zones">No zones yet</p>
                ) : (
                  zones.map((zone, idx) => (
                    <div key={idx} className="zone-item">
                      <span 
                        className="zone-color" 
                        style={{ backgroundColor: zoneColors[idx % zoneColors.length] }}
                      />
                      <span className="zone-name">{zone.name}</span>
                      <span className="zone-points">({zone.polygon.length} points)</span>
                      <button onClick={() => deleteZone(idx)} className="delete-zone">
                        🗑️
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>

            <div className="control-section instructions">
              <h3>📝 Instructions</h3>
              <ul>
                <li><strong>Left Click:</strong> Add point to zone</li>
                <li><strong>Right Click:</strong> Complete zone (min 3 points)</li>
                <li><strong>Undo:</strong> Remove last point</li>
                <li>Draw at least one zone before saving</li>
              </ul>
            </div>

            <div className="control-section save-section">
              <button onClick={handleSave} className="btn-save">
                💾 Save Zones
              </button>
              <button onClick={onCancel} className="btn-cancel">
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ZoneDrawer;
