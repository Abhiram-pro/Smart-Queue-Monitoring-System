# Backend - Smart Queue Monitoring System

Python backend for queue detection and WebSocket server.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python scripts/start_api.sh
```

## Deploy to Railway/Render

1. Push to GitHub
2. Create new project on Railway or Render
3. Set environment variable: `PORT=5000`
4. Deploy

## Configuration

Edit `config/zones.json` to configure monitoring zones.
