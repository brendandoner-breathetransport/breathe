# Deploy FastAPI Backend (Render)

This deploys `civic_affordability_pg/api/main.py` as a public backend for the Vercel frontend.

## 1) Create a Render Web Service

- Render Dashboard -> New -> Web Service
- Connect repo: `BDickerson89/breathe`
- Branch: `vercel-main` (or your active deployment branch)
- Root Directory: `civic_affordability_pg/api`

## 2) Use these service commands

- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 3) Add environment variable

- Key: `DATABASE_URL`
- Value: your Supabase Postgres URL

Recommended Supabase format:

`postgresql://postgres:<PASSWORD>@db.wtfcubbiyglhsywrbkgf.supabase.co:5432/postgres?sslmode=require`

## 4) Deploy and test

After deploy, verify:

- `/health`
- `/api/affordability?state_abbrev=CO`
- `/api/policy?state_abbrev=CO`

## 5) Wire Vercel frontend

In Vercel env vars set:

- `BACKEND_API_BASE_URL=https://<your-render-service>.onrender.com`

Then redeploy frontend.
