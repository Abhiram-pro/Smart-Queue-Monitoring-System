# Test Your App - Step by Step

## ✅ Servers Running

- Backend: http://localhost:8000 ✅
- Frontend: http://localhost:3000 ✅

## 🧪 Test Steps

### Test 1: Backend Health Check

Open a new browser tab and go to:
```
http://localhost:8000
```

**Expected Result:**
```json
{
  "status": "running",
  "service": "Smart Queue Monitoring System",
  "version": "1.0.0"
}
```

If you see this ✅ Backend is working!

---

### Test 2: Frontend Loading

Open a new browser tab and go to:
```
http://localhost:3000
```

**Expected Result:**
You should see a page with:
- Title: "🎯 Smart Queue Monitoring System"
- Connection status in top right (should say "Connected" with green dot)
- Three buttons in the middle
- A warning message about zones

If you see this ✅ Frontend is working!

---

### Test 3: WebSocket Connection

Look at the connection status in the top right corner of http://localhost:3000

**Expected Result:**
- Green dot
- Text says "Connected"

If you see this ✅ WebSocket is working!

---

### Test 4: Start Camera (Demo Mode)

1. Go to http://localhost:3000
2. You'll see a warning: "⚠️ No zones configured"
3. The "Start Camera" button will be disabled

**To enable it:**
1. Click "🎨 Configure Zones"
2. Even though no frame shows, click outside or press ESC
3. OR manually enable zones by creating a config file

**Alternative - Skip zone requirement:**
Let me create a version that works without zones for demo...

---

## 🐛 If Something's Not Working

### Frontend shows "Disconnected"
- Check if backend is running: http://localhost:8000
- Check browser console (F12) for errors

### Page is blank
- Check if frontend compiled successfully
- Look for errors in the terminal where you ran `npm start`

### Buttons don't work
- Open browser console (F12)
- Click a button
- Check for JavaScript errors

---

## 💡 Quick Fix - Enable Demo Mode

Let me update the backend to automatically mark zones as configured for demo purposes...
