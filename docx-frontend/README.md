# DocX Frontend

Premium React/Vite frontend for the FastAPI Document Intelligence Engine.

## Requirements
- Node.js 18+ (20+ recommended)
- Backend running at http://localhost:8000

## Run
```bash
npm install
npm run dev
```

Open http://localhost:5173

The Vite development proxy maps `/api/*` to `http://localhost:8000/*`, so no CORS configuration is needed during local development.

## Connected backend endpoints
- `POST /upload` — PDF/JPEG/PNG ingestion
- `POST /search` — semantic search

The UI is intentionally compatible with the current repository API and does not invent endpoints that the backend does not provide.
