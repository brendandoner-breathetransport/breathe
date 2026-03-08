# Vercel Setup

## 1) Push to GitHub

Push this repository so Vercel can import it.

## 2) Create project in Vercel

- Vercel Dashboard -> `Add New...` -> `Project`
- Import your repo
- Set **Root Directory** to:
  - `civic_affordability_pg/frontend`

Framework should auto-detect as Next.js.

## 3) Add environment variable

In Project Settings -> Environment Variables, add:

- `BACKEND_API_BASE_URL`
  - Example: `https://your-fastapi-service.example.com`
  - No trailing slash

Apply to `Production`, `Preview`, and optionally `Development`.

## 4) Deploy

Trigger deploy from Vercel UI or by pushing to your tracked branch.

After deployment verify:
- `/`
- `/state/co`
- `GET /api/affordability?state_abbrev=CO`
- `GET /api/policy?state_abbrev=CO`

## 5) Custom domain (optional)

Project -> Settings -> Domains -> add domain.

## Notes

- Keep Postgres credentials only in backend service env, not in Vercel frontend env.
- Vercel only needs `BACKEND_API_BASE_URL`.
