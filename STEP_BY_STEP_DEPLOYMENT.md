# 🚀 Law Analyse - Automated Deployment Guide

## IMPORTANT: Manual Steps Required

These steps require your authentication and cannot be automated. Follow each step carefully.

---

## ✅ STEP 1: Configure GitHub Repository (5 minutes)

### 1.1 Add Topics

**Action:** Open in browser
```
https://github.com/nposeo/law-analyse
```

**Steps:**
1. Click "⚙️" (gear icon) next to "About" section (top right)
2. In "Topics" field, add these topics (press Enter after each):
   ```
   legal-tech
   ai
   nlp
   ukrainian-law
   fastapi
   astro
   react
   typescript
   python
   openai
   gpt-4
   langchain
   postgresql
   docker
   ```
3. In "Description" field, paste:
   ```
   AI-powered Ukrainian law analysis platform with GPT-4o
   ```
4. Click "Save changes"

### 1.2 Configure Secrets

**Action:** Open in browser
```
https://github.com/nposeo/law-analyse/settings/secrets/actions
```

**Steps:**
1. Click "New repository secret"
2. Name: `OPENAI_API_KEY`
3. Value: Your OpenAI API key from https://platform.openai.com/api-keys
4. Click "Add secret"

**Note:** If you don't have an OpenAI API key:
- Go to: https://platform.openai.com/api-keys
- Click "Create new secret key"
- Copy the key (shown only once!)
- Paste into GitHub secret

### 1.3 Enable GitHub Actions

**Action:** Open in browser
```
https://github.com/nposeo/law-analyse/actions
```

**Steps:**
1. If prompted, click "I understand my workflows, go ahead and enable them"
2. Verify these workflows are listed:
   - Backend Tests
   - Frontend Build
   - Docker Build

### 1.4 Enable Discussions (Optional)

**Action:** Open in browser
```
https://github.com/nposeo/law-analyse/settings
```

**Steps:**
1. Scroll to "Features" section
2. Check ✅ "Discussions"
3. Scroll down and click "Save changes"

**✅ Step 1 Complete!** GitHub is now configured.

---

## ✅ STEP 2: Create GitHub Release v1.0.0 (5 minutes)

### 2.1 Create Release

**Action:** Open in browser
```
https://github.com/nposeo/law-analyse/releases/new
```

### 2.2 Fill Release Form

**Tag version:**
```
v1.0.0
```

**Target:** `main` (default)

**Release title:**
```
Law Analyse MVP v1.0.0
```

**Description:** Copy this text:

```markdown
# Law Analyse MVP v1.0.0

First production-ready release of Law Analyse - AI-powered Ukrainian law analysis platform.

## ✨ Features

- **PDF Parsing** - Extract articles from Ukrainian law PDFs
- **AI Extraction** - 2-agent adversarial review using GPT-4o
- **Structured Data** - PostgreSQL storage with SQLAlchemy ORM
- **REST API** - FastAPI backend with OpenAPI docs
- **Interactive Frontend** - Astro + React with collapsible article tree
- **Plain Language Mode** - Toggle between legal and simplified text
- **Confidence Scoring** - Auto-flag low-confidence extractions
- **Background Processing** - Async PDF processing
- **Docker Support** - Multi-stage builds
- **CI/CD** - GitHub Actions workflows

## 🎓 Tech Stack

**Backend:** FastAPI + Python 3.11 + pdfplumber + LangChain + PostgreSQL  
**Frontend:** Astro + React + TypeScript + Tailwind CSS  
**AI:** OpenAI GPT-4o with 2-agent adversarial review  
**DevOps:** Docker + GitHub Actions

## 📊 Statistics

- **23 commits** (all from nposeo)
- **78 files** (29 code + 26 docs + 23 config)
- **~5,000 lines of code**
- **Development time:** ~4.5 hours
- **Cost:** $0 development + $0/month hosting

## 🚀 Quick Start

```bash
git clone https://github.com/nposeo/law-analyse.git
cd law-analyse
./setup.sh  # or setup.bat on Windows
./dev.sh    # or dev.bat on Windows
```

**Frontend:** http://localhost:4321  
**Backend API:** http://localhost:8000  
**API Docs:** http://localhost:8000/docs

## 📖 Documentation

- [Quick Start Guide](https://github.com/nposeo/law-analyse/blob/main/QUICKSTART.md)
- [Deployment Guide](https://github.com/nposeo/law-analyse/blob/main/DEPLOYMENT.md)
- [Docker Guide](https://github.com/nposeo/law-analyse/blob/main/DOCKER.md)
- [Developer Reference](https://github.com/nposeo/law-analyse/blob/main/DEV_REFERENCE.md)

## 💰 Cost

- **Development:** $0 (open-source stack)
- **Hosting:** $0/month (Railway + Vercel + Neon free tiers)
- **AI Processing:** $5-10 per law (one-time)

## 🎯 Roadmap

**v1.1.0** (2 weeks) - 5-10 popular laws, full-text search, export  
**v1.2.0** (1 month) - User auth, admin panel, bookmarks  
**v2.0.0** (3 months) - Auto-scraping, version comparison, mobile app

## 📝 License

MIT License - see [LICENSE](https://github.com/nposeo/law-analyse/blob/main/LICENSE)

## 📞 Support

- **Issues:** https://github.com/nposeo/law-analyse/issues
- **Discussions:** https://github.com/nposeo/law-analyse/discussions
- **Email:** nposeo@gmail.com

---

**Making Ukrainian laws accessible to everyone through AI.**

🚀 **Ready for Production Deployment!**
```

### 2.3 Publish Release

**Steps:**
1. Check ✅ "Set as the latest release"
2. Click "Publish release" (green button)

### 2.4 Verify Release

**Action:** Open in browser
```
https://github.com/nposeo/law-analyse/releases
```

**Verify:**
- ✅ v1.0.0 is published
- ✅ Release notes display correctly
- ✅ Tag created

**✅ Step 2 Complete!** Release v1.0.0 is live.

---

## ✅ STEP 3: Deploy to Production (1-2 hours)

### 3.1 Deploy Database (Neon PostgreSQL) - 10 minutes

**Action:** Open in browser
```
https://console.neon.tech/signup
```

**Steps:**
1. Create account (or login if you have one)
2. Click "Create a project"
3. Fill in:
   - **Name:** `law-analyse-db`
   - **Region:** Choose closest to your users (e.g., Europe for Ukraine)
   - **PostgreSQL version:** 16 (latest)
4. Click "Create project"
5. Wait for project to be created (~30 seconds)
6. Copy connection string:
   - Click "Connection string" tab
   - Copy the string that looks like:
     ```
     postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb
     ```
7. **SAVE THIS STRING** - you'll need it for Railway

**✅ Database Created!** Connection string saved.

### 3.2 Deploy Backend (Railway) - 15-20 minutes

**Action:** Open in browser
```
https://railway.app/new
```

**Steps:**
1. Create account (or login)
2. Click "Deploy from GitHub repo"
3. If prompted, connect your GitHub account
4. Select repository: `nposeo/law-analyse`
5. Click "Deploy Now"
6. Wait for initial deployment (~2 minutes)
7. Click on the deployed service
8. Click "Settings" tab
9. Scroll to "Root Directory"
   - Set to: `backend`
   - Click "Update"
10. Click "Variables" tab
11. Add environment variables (click "+ New Variable" for each):
    
    **DATABASE_URL:**
    ```
    postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb
    ```
    (paste your Neon connection string)
    
    **OPENAI_API_KEY:**
    ```
    sk-...
    ```
    (your OpenAI API key)
    
    **PORT:**
    ```
    8000
    ```
    
    **CORS_ORIGINS:**
    ```
    https://law-analyse.vercel.app
    ```
    (we'll update this after Vercel deployment)

12. Click "Deploy" to redeploy with new variables
13. Wait for deployment (~3 minutes)
14. Click "Settings" → "Networking"
15. Click "Generate Domain"
16. **COPY THE URL** (e.g., `https://law-analyse-backend.up.railway.app`)
17. **SAVE THIS URL** - you'll need it for Vercel

**Test Backend:**
Open in browser:
```
https://law-analyse-backend.up.railway.app/docs
```
You should see the FastAPI documentation page.

**✅ Backend Deployed!** URL saved.

### 3.3 Run Database Migrations - 5 minutes

**Action:** On your local machine, open terminal

**Steps:**
1. Set DATABASE_URL environment variable:
   
   **Windows (CMD):**
   ```bash
   set DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb
   ```
   
   **Windows (PowerShell):**
   ```bash
   $env:DATABASE_URL="postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb"
   ```
   
   **Linux/Mac:**
   ```bash
   export DATABASE_URL="postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb"
   ```

2. Navigate to backend directory:
   ```bash
   cd D:\server\OpenServer\domains\LawAnalyse\www\backend
   ```

3. Activate virtual environment:
   
   **Windows:**
   ```bash
   .venv\Scripts\activate
   ```
   
   **Linux/Mac:**
   ```bash
   source .venv/bin/activate
   ```

4. Run migrations:
   ```bash
   alembic upgrade head
   ```

5. Verify tables created:
   ```bash
   psql "postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb" -c "\dt"
   ```
   
   You should see tables: `laws`, `articles`, `norms`, `alembic_version`

**✅ Database Migrated!** Tables created.

### 3.4 Deploy Frontend (Vercel) - 10-15 minutes

**Action:** Open in browser
```
https://vercel.com/signup
```

**Steps:**
1. Create account (or login)
2. Click "Add New..." → "Project"
3. Click "Import Git Repository"
4. If prompted, connect your GitHub account
5. Find and select: `nposeo/law-analyse`
6. Click "Import"
7. Configure project:
   - **Framework Preset:** Astro (should auto-detect)
   - **Root Directory:** Click "Edit" → Enter `frontend` → Click "Continue"
   - **Build Command:** `npm run build` (default)
   - **Output Directory:** `dist` (default)
8. Click "Environment Variables"
9. Add variable:
   - **Key:** `PUBLIC_API_URL`
   - **Value:** `https://law-analyse-backend.up.railway.app`
     (your Railway backend URL)
10. Click "Deploy"
11. Wait for deployment (~3-5 minutes)
12. **COPY THE URL** (e.g., `https://law-analyse.vercel.app`)

**✅ Frontend Deployed!** URL saved.

### 3.5 Update Backend CORS - 2 minutes

**Action:** Go back to Railway

**Steps:**
1. Open: https://railway.app
2. Click on your `law-analyse` project
3. Click on the backend service
4. Click "Variables" tab
5. Find `CORS_ORIGINS` variable
6. Click "Edit"
7. Update value to your Vercel URL:
   ```
   https://law-analyse.vercel.app
   ```
8. Click "Update"
9. Service will automatically redeploy (~1 minute)

**✅ CORS Updated!** Frontend can now call backend.

### 3.6 Test Deployment - 5 minutes

**Action:** Open your frontend URL in browser
```
https://law-analyse.vercel.app
```

**Verify:**
- ✅ Page loads without errors
- ✅ No console errors (press F12 → Console tab)
- ✅ API connection works

**Test API directly:**
```
https://law-analyse-backend.up.railway.app/docs
```

**✅ Deployment Complete!** All services running.

---

## ✅ STEP 4: Test End-to-End (Optional - 30-60 minutes)

### 4.1 Download Test Law

**Action:** Open in browser
```
https://zakon.rada.gov.ua/laws/show/2145-19
```

**Steps:**
1. Find download link for PDF
2. Save as: `zakon_pro_osvitu.pdf`

### 4.2 Upload Law

**Option A: Via Frontend**
1. Open: `https://law-analyse.vercel.app`
2. Click "Upload Law" button
3. Fill in form:
   - File: `zakon_pro_osvitu.pdf`
   - Title: `Закон України про освіту`
   - Document Number: `2145-VIII`
   - Publication Date: `2017-09-05`
4. Submit

**Option B: Via API**
```bash
curl -X POST "https://law-analyse-backend.up.railway.app/laws/upload" \
  -F "file=@zakon_pro_osvitu.pdf" \
  -F "title=Закон України про освіту" \
  -F "document_number=2145-VIII" \
  -F "publication_date=2017-09-05"
```

### 4.3 Process Law

**Via API:**
```bash
curl -X POST "https://law-analyse-backend.up.railway.app/process/{law_id}"
```

**Monitor status:**
```bash
curl "https://law-analyse-backend.up.railway.app/process/{law_id}/status"
```

Wait ~5-10 minutes for processing to complete.

### 4.4 View Results

**Action:** Open in browser
```
https://law-analyse.vercel.app/law/{law_id}
```

**Verify:**
- ✅ Law metadata displays
- ✅ Article tree renders
- ✅ Articles expand/collapse
- ✅ Plain language toggle works
- ✅ Confidence scores display
- ✅ Low-confidence articles flagged

**✅ End-to-End Test Complete!**

---

## 📊 DEPLOYMENT SUMMARY

### URLs
```
Repository:  https://github.com/nposeo/law-analyse
Frontend:    https://law-analyse.vercel.app
Backend:     https://law-analyse-backend.up.railway.app
API Docs:    https://law-analyse-backend.up.railway.app/docs
Database:    [Neon Console]
```

### Credentials (Save Securely!)
```
Neon:
- Connection String: postgresql://...
- Console: https://console.neon.tech

Railway:
- Project: https://railway.app/project/...

Vercel:
- Project: https://vercel.com/nposeo/law-analyse

OpenAI:
- API Key: sk-...
- Dashboard: https://platform.openai.com
```

### Costs
```
Development:  $0
Hosting:      $0/month (free tiers)
AI Processing: $5-10 per law (one-time)
Total:        $5-10 for testing
```

---

## 🎉 CONGRATULATIONS!

**Law Analyse MVP is now LIVE in production!**

### What You've Accomplished:
✅ Configured GitHub repository  
✅ Created Release v1.0.0  
✅ Deployed database (Neon)  
✅ Deployed backend (Railway)  
✅ Deployed frontend (Vercel)  
✅ Tested end-to-end  

### Next Steps:
1. Share on social media
2. Post in communities
3. Gather feedback
4. Add more laws
5. Iterate and improve

---

**Made with ❤️ for Ukraine**

🇺🇦 **Making Ukrainian laws accessible to everyone through AI**

🚀 **Project Complete!**
