# Smart Queue Monitoring System

AI-powered real-time queue monitoring with React dashboard.

## Project Structure

```
├── frontend/          # React TypeScript app
│   ├── src/          # React components
│   ├── public/       # Static assets
│   └── package.json  # Dependencies
│
└── backend/          # Python backend
    ├── scripts/      # Python scripts
    ├── config/       # Configuration
    ├── data/         # Data storage
    └── requirements.txt
```

## Quick Start

### Frontend
```bash
cd frontend
npm install
npm start
```

### Backend
```bash
cd backend
pip install -r requirements.txt
python scripts/start_api.sh
```

## Deployment

### Frontend → Vercel
```bash
cd frontend
vercel --prod
```

### Backend → Railway/Render
Deploy the `backend/` folder to Railway or Render.

See individual README files in each folder for details.

## License

See LICENSE file.
