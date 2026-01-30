# Deploy Backend to Railway

## Step-by-Step Guide

### 1. Go to Railway

Visit: https://railway.app

### 2. Create New Project

- Click "New Project"
- Select "Deploy from GitHub repo"
- Authorize Railway to access your GitHub
- Select repository: `Smart-Queue-Monitoring-System`

### 3. Configure Root Directory

**IMPORTANT:** Railway needs to know to deploy only the backend folder.

- After selecting the repo, Railway will start deploying
- Click on your service
- Go to "Settings" tab
- Find "Root Directory" setting
- Set it to: `backend`
- Click "Save"

### 4. Verify Deployment

- Go to "Deployments" tab
- Wait for build to complete (2-3 minutes)
- Once deployed, you'll see a URL like: `https://your-app.railway.app`

### 5. Test Your Backend

Click on the Railway URL or visit it in browser. You should see:

```json
{
  "status": "running",
  "service": "Smart Queue Monitoring System",
  "version": "1.0.0"
}
```

### 6. Copy Your Backend URL

Copy the full URL (e.g., `https://smart-queue-monitoring-system-production.up.railway.app`)

You'll need this for the frontend deployment!

## Troubleshooting

### Build fails?
- Check "Logs" tab in Railway
- Verify `backend/requirements.txt` exists
- Ensure Root Directory is set to `backend`

### Server not starting?
- Check if `PORT` environment variable is set (Railway sets this automatically)
- View logs for error messages

## Next Steps

After backend is deployed:
1. Copy your Railway URL
2. Deploy frontend to Vercel
3. Set environment variables in Vercel with your Railway URL

See `DEPLOYMENT.md` for frontend deployment instructions.
