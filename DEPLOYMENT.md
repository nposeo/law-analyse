# Law Analyse MVP - Deployment Guide

## Prerequisites

1. **Accounts needed:**
   - GitHub account (for code hosting)
   - Railway account (backend hosting) - https://railway.app
   - Vercel account (frontend hosting) - https://vercel.com
   - Neon account (PostgreSQL database) - https://neon.tech
   - OpenAI account with API key - https://platform.openai.com

## Step 1: Database Setup (Neon PostgreSQL)

1. Go to https://neon.tech and create account
2. Create new project: "law-analyse-db"
3. Copy connection string (looks like: `postgresql://user:pass@host/dbname`)
4. Save it for later use

## Step 2: Push to GitHub

```bash
# Make sure you're in project root
cd D:\server\OpenServer\domains\LawAnalyse\www

# Authenticate with GitHub CLI
gh auth login

# Create repository and push
gh repo create law-analyse --public --source=. --push

# Verify
gh repo view --web
```

## Step 3: Backend Deployment (Railway)

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `law-analyse` repository
4. Railway will auto-detect Python and create service
5. Add environment variables in Railway dashboard:
   - `DATABASE_URL` = (your Neon connection string)
   - `OPENAI_API_KEY` = (your OpenAI API key)
   - `ENVIRONMENT` = `production`
6. Railway will auto-deploy
7. Copy the generated URL (e.g., `https://law-analyse-production.up.railway.app`)

## Step 4: Run Database Migrations

```bash
# Install dependencies locally
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Set DATABASE_URL
export DATABASE_URL="your-neon-connection-string"

# Run migrations
alembic upgrade head
```

## Step 5: Frontend Deployment (Vercel)

1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Import `law-analyse` from GitHub
4. Configure build settings:
   - **Framework Preset:** Astro
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Add environment variable:
   - `PUBLIC_API_URL` = (your Railway backend URL)
6. Click "Deploy"
7. Vercel will build and deploy
8. Copy the generated URL (e.g., `https://law-analyse.vercel.app`)

## Step 6: Test the Application

1. **Upload test law PDF:**
   ```bash
   curl -X POST "https://your-backend.railway.app/laws/upload" \
     -F "file=@path/to/law.pdf" \
     -F "title=Закон України про освіту"
   ```

2. **Trigger processing:**
   ```bash
   curl -X POST "https://your-backend.railway.app/process/{law_id}"
   ```

3. **Check status:**
   ```bash
   curl "https://your-backend.railway.app/process/{law_id}/status"
   ```

4. **View in frontend:**
   - Open `https://law-analyse.vercel.app`
   - Click on the law
   - Navigate through articles

## Step 7: Download Test Law

Download "Закон України про освіту" from:
https://zakon.rada.gov.ua/laws/show/2145-19

Or use curl:
```bash
curl -o education_law.pdf "https://zakon.rada.gov.ua/laws/show/2145-19/print"
```

## Troubleshooting

### Backend not starting
- Check Railway logs for errors
- Verify DATABASE_URL is correct
- Ensure OPENAI_API_KEY is valid

### Frontend can't connect to backend
- Verify PUBLIC_API_URL in Vercel environment variables
- Check CORS settings in backend (should include Vercel URL)
- Test backend health: `curl https://your-backend.railway.app/health`

### Database connection errors
- Verify Neon database is active
- Check connection string format
- Ensure migrations were run

### PDF processing fails
- Check OpenAI API key has credits
- Verify PDF is valid Ukrainian law document
- Check Railway logs for detailed error messages

## Cost Estimates

- **Railway:** Free tier ($5 credit/month) - sufficient for MVP
- **Vercel:** Free tier - sufficient for MVP
- **Neon:** Free tier (0.5GB) - sufficient for MVP
- **OpenAI API:** ~$5-10 per law (40 articles × 2 agents × $0.03/1K tokens)

**Total:** ~$5-10 one-time for processing test law, $0/month recurring

## Next Steps After Deployment

1. Process "Закон про освіту" through the system
2. Manually verify accuracy on 20 random articles
3. Document any systematic errors for prompt tuning
4. Share with test users for feedback
5. Monitor OpenAI API costs and processing times

## Production Considerations

For scaling beyond MVP:

1. **Add authentication** (Clerk, Auth0, or custom)
2. **Implement caching** (Redis for processed laws)
3. **Add job queue** (Celery, BullMQ for background processing)
4. **Set up monitoring** (Sentry for errors, Datadog for metrics)
5. **Implement rate limiting** (to prevent API abuse)
6. **Add admin panel** for human review workflow
7. **Set up CI/CD** (GitHub Actions for automated testing/deployment)
