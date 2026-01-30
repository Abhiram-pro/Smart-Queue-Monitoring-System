# Backend - Smart Queue Monitoring System

Python Flask + WebSocket server for real-time queue monitoring.

## Local Setup

```bash
pip install -r requirements.txt
python server.py
```

Server runs on `http://localhost:5000`

## Deploy to Railway

### Option 1: Via Railway Dashboard

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Select "backend" as root directory
6. Railway will auto-detect Python and deploy
7. Add environment variable (optional): `PORT=5000`
8. Click "Deploy"

### Option 2: Via Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up
```

## Environment Variables

- `PORT`: Server port (default: 5000, Railway sets this automatically)

## API Endpoints

- `GET /` - Health check
- `GET /api/health` - Health status
- `GET /api/config` - Get zone configuration
- WebSocket: Connect to root URL for real-time updates

## After Deployment

Copy your Railway URL (e.g., `https://your-app.railway.app`) and use it in the frontend environment variables:
- `REACT_APP_API_URL=https://your-app.railway.app`
- `REACT_APP_WS_URL=wss://your-app.railway.app`
