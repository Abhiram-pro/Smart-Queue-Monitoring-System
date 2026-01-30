"""
Real-time Queue Monitoring with YOLO Detection
Captures video from camera, detects people, tracks them, and sends data to dashboard
"""

import cv2
import numpy as np
from ultralytics import YOLO
import json
import time
import base64
from collections import defaultdict
import os

class QueueMonitor:
    def __init__(self, socketio, config_path='config/zones.json'):
        self.socketio = socketio
        self.config_path = config_path
        self.model = None
        self.camera = None
        self.running = False
        self.zones = []
        self.tracked_objects = {}
        self.frame_count = 0
        
    def load_model(self):
        """Load YOLO model"""
        print("📦 Loading YOLO model...")
        try:
            self.model = YOLO('yolov8n.pt')  # Nano model for speed
            print("✅ YOLO model loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to load YOLO model: {e}")
            print("💡 Downloading model... This may take a minute...")
            try:
                self.model = YOLO('yolov8n.pt')
                print("✅ Model downloaded and loaded")
                return True
            except Exception as e2:
                print(f"❌ Failed to download model: {e2}")
                return False
    
    def load_zones(self):
        """Load zone configuration"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.zones = config.get('zones', [])
                print(f"✅ Loaded {len(self.zones)} zones")
                return True
            else:
                print("⚠️ No zones configured")
                return False
        except Exception as e:
            print(f"❌ Failed to load zones: {e}")
            return False
    
    def start_camera(self, camera_id=0):
        """Start camera capture"""
        print(f"📹 Starting camera {camera_id}...")
        try:
            self.camera = cv2.VideoCapture(camera_id)
            if not self.camera.isOpened():
                print("❌ Failed to open camera")
                return False
            
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            print("✅ Camera started successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to start camera: {e}")
            return False
    
    def point_in_polygon(self, point, polygon):
        """Check if point is inside polygon using ray casting"""
        x, y = point
        n = len(polygon)
        inside = False
        
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def get_zone_for_point(self, point):
        """Get zone name for a point"""
        for zone in self.zones:
            polygon = [(p[0], p[1]) for p in zone['polygon']]
            if self.point_in_polygon(point, polygon):
                return zone['name']
        return 'Unknown'
    
    def process_frame(self, frame):
        """Process single frame with YOLO detection"""
        # Run YOLO detection
        results = self.model(frame, conf=0.45, classes=[0])  # class 0 = person
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0])
                
                # Calculate center point
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                
                # Get zone
                zone = self.get_zone_for_point((center_x, center_y))
                
                detections.append({
                    'bbox': [int(x1), int(y1), int(x2), int(y2)],
                    'confidence': conf,
                    'center': (center_x, center_y),
                    'zone': zone
                })
        
        return detections
    
    def draw_detections(self, frame, detections):
        """Draw bounding boxes and zones on frame"""
        # Draw zones
        for zone in self.zones:
            polygon = np.array(zone['polygon'], np.int32)
            cv2.polylines(frame, [polygon], True, (0, 255, 0), 2)
            
            # Draw zone name
            if len(polygon) > 0:
                cv2.putText(frame, zone['name'], tuple(polygon[0]), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Draw detections
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            conf = det['confidence']
            zone = det['zone']
            
            # Draw bounding box
            color = (0, 255, 0) if zone != 'Unknown' else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"{zone} {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Draw center point
            cv2.circle(frame, det['center'], 5, (255, 0, 0), -1)
        
        return frame
    
    def calculate_statistics(self, detections):
        """Calculate queue statistics"""
        zone_counts = defaultdict(int)
        for det in detections:
            zone_counts[det['zone']] += 1
        
        # Separate by zone type
        in_queue = sum(count for zone, count in zone_counts.items() 
                      if 'queue' in zone.lower())
        at_cashdesk = sum(count for zone, count in zone_counts.items() 
                         if 'cashdesk' in zone.lower() or 'caisse' in zone.lower())
        
        total_people = len(detections)
        
        # Mock wait times (would need tracking for real values)
        avg_wait_time = int(in_queue * 15) if in_queue > 0 else 0
        max_wait_time = int(avg_wait_time * 1.5) if avg_wait_time > 0 else 0
        
        return {
            'totalPeople': total_people,
            'inQueue': in_queue,
            'atCashdesk': at_cashdesk,
            'completed': 0,  # Would need tracking
            'avgWaitTime': avg_wait_time,
            'maxWaitTime': max_wait_time,
            'alerts': 1 if in_queue > 5 else 0
        }
    
    def create_customers_list(self, detections):
        """Create customer list from detections"""
        customers = []
        for i, det in enumerate(detections):
            wait_time = np.random.randint(10, 120)  # Mock wait time
            status = 'alert' if wait_time > 90 else 'waiting' if 'queue' in det['zone'].lower() else 'serving'
            
            customers.append({
                'id': i + 1,
                'zone': det['zone'],
                'waitTime': wait_time,
                'status': status,
                'hasAlert': wait_time > 90
            })
        
        return customers
    
    def frame_to_base64(self, frame):
        """Convert frame to base64 for transmission"""
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        return jpg_as_text
    
    def run(self):
        """Main monitoring loop"""
        print("🚀 Starting queue monitoring...")
        self.running = True
        self.frame_count = 0
        
        # Load model and zones
        if not self.load_model():
            self.socketio.emit('error', {'message': 'Failed to load AI model'})
            return
        
        if not self.load_zones():
            self.socketio.emit('error', {'message': 'No zones configured'})
            return
        
        # Start camera
        if not self.start_camera():
            self.socketio.emit('error', {'message': 'Failed to start camera'})
            return
        
        # Notify camera started
        self.socketio.emit('camera_started')
        
        try:
            while self.running:
                ret, frame = self.camera.read()
                if not ret:
                    print("❌ Failed to read frame")
                    break
                
                self.frame_count += 1
                
                # Process every 2nd frame for performance
                if self.frame_count % 2 != 0:
                    continue
                
                # Detect people
                detections = self.process_frame(frame)
                
                # Draw on frame
                annotated_frame = self.draw_detections(frame.copy(), detections)
                
                # Calculate statistics
                stats = self.calculate_statistics(detections)
                
                # Create customer list
                customers = self.create_customers_list(detections)
                
                # Convert frame to base64
                frame_base64 = self.frame_to_base64(annotated_frame)
                
                # Send update to dashboard
                data = {
                    'frame': self.frame_count,
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'stats': stats,
                    'customers': customers,
                    'videoFrame': frame_base64
                }
                
                self.socketio.emit('queue_update', data)
                
                # Small delay to control frame rate
                time.sleep(0.033)  # ~30 FPS
                
        except Exception as e:
            print(f"❌ Error in monitoring loop: {e}")
            self.socketio.emit('error', {'message': str(e)})
        finally:
            self.stop()
    
    def stop(self):
        """Stop monitoring"""
        print("⏹️ Stopping queue monitoring...")
        self.running = False
        if self.camera:
            self.camera.release()
        self.socketio.emit('camera_stopped')
        print("✅ Monitoring stopped")
    
    def capture_frame_for_zones(self):
        """Capture a single frame for zone configuration"""
        print("📸 Capturing frame for zone configuration...")
        
        if not self.camera or not self.camera.isOpened():
            if not self.start_camera():
                return None
        
        ret, frame = self.camera.read()
        if not ret:
            print("❌ Failed to capture frame")
            return None
        
        # Convert to base64
        frame_base64 = self.frame_to_base64(frame)
        
        # Release camera
        self.camera.release()
        self.camera = None
        
        return frame_base64
