# Frontend (Next.js)

## Local setup

```bash
cd /Users/brentondickerson/git/breathe/civic_affordability_pg/frontend
cp .env.example .env.local
# set BACKEND_API_BASE_URL to your running FastAPI URL
npm install
npm run dev
```

Open:
- `/`
- `/state/co`

## API proxy behavior

Frontend route handlers proxy to `BACKEND_API_BASE_URL`:
- `GET /api/affordability`
- `GET /api/policy`
- `POST /api/ask`

CSV downloads are available via:
- `/api/affordability?state_abbrev=CO&format=csv`
- `/api/policy?state_abbrev=CO&format=csv`

## Vercel

See `VERCEL_SETUP.md`.
