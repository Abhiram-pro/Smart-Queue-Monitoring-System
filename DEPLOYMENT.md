# Deployment Guide

## Frontend (Vercel)

1. Navigate to frontend folder:
```bash
cd frontend
```

2. Deploy:
```bash
vercel --prod
```

3. After deployment, add environment variables in Vercel dashboard:
   - `REACT_APP_API_URL`: Your backend URL
   - `REACT_APP_WS_URL`: Your WebSocket URL

## Backend (Railway)

1. Go to https://railway.app
2. Create new project from GitHub
3. Select the `backend` folder as root directory
4. Add environment variable: `PORT=5000`
5. Deploy

## Backend (Render)

1. Go to https://render.com
2. Create new Web Service
3. Root directory: `backend`
4. Build command: `pip install -r requirements.txt`
5. Start command: `python scripts/start_api.sh`
6. Deploy

## Connect Frontend to Backend

After both are deployed:
1. Go to Vercel dashboard
2. Settings → Environment Variables
3. Add backend URLs
4. Redeploy frontend
