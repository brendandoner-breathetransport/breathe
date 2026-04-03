# Deploy Breathe Dashboard to Render

## Free plan notes
- Free web services **spin down after 15 min of inactivity** — first request after that
  takes ~30–60 s to wake up.
- Paid Starter ($7/month) keeps the service always on.

---

## Option A — Auto-deploy via render.yaml (recommended)

The repo already has `civic_affordability_pg/render.yaml` with a `breathe-dashboard`
service entry. Render will pick this up automatically if you connect the repo.

1. Go to **Render Dashboard → New → Blueprint**
2. Connect your GitHub repo (`brendandoner-breathetransport/breathe` or wherever it lives)
3. Render reads `civic_affordability_pg/render.yaml` and creates the `breathe-dashboard` service
4. Hit **Apply** — Render builds and deploys automatically

---

## Option B — Manual web service

1. **Render Dashboard → New → Web Service**
2. Connect your GitHub repo
3. Set these fields:

| Field | Value |
|---|---|
| **Root Directory** | *(leave blank — repo root)* |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r breathe_fastapi/requirements.txt` |
| **Start Command** | `uvicorn breathe_fastapi.main:app --host 0.0.0.0 --port $PORT` |

4. No environment variables needed.
5. Click **Create Web Service**.

---

## Verify after deploy

Once live (URL looks like `https://breathe-dashboard.onrender.com`), check:

- `https://<your-service>.onrender.com/` — dashboard homepage
- `https://<your-service>.onrender.com/api/countries` — should return JSON list
- `https://<your-service>.onrender.com/api/economy/income?dark_mode=light&income_level=Bottom+50%25&country=usa`
