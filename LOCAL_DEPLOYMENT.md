# 🐳 Law Analyse - Local Docker Deployment Guide

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- OpenAI API key

---

## Step 1: Start Docker Desktop

**Windows:**
1. Open Start Menu
2. Search for "Docker Desktop"
3. Click to start
4. Wait for Docker icon in system tray to show "Docker Desktop is running"

**Or run from command line:**
```bash
"C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

---

## Step 2: Configure Environment Variables

### Edit `.env` file in project root:

```bash
# Open in notepad
notepad .env
```

**Replace this line:**
```
OPENAI_API_KEY=your-openai-api-key-here
```

**With your actual OpenAI API key:**
```
OPENAI_API_KEY=sk-proj-...
```

**Get your API key from:** https://platform.openai.com/api-keys

**Save and close the file.**

---

## Step 3: Start All Services

```bash
docker-compose up -d
```

This will:
- Pull PostgreSQL image
- Build backend Docker image (~2-3 minutes)
- Build frontend Docker image (~2-3 minutes)
- Start all services

**Expected output:**
```
Creating network "lawanalyse_default" with the default driver
Creating volume "lawanalyse_postgres_data" with default driver
Creating law-analyse-db ... done
Creating law-analyse-backend ... done
Creating law-analyse-frontend ... done
```

---

## Step 4: Check Services Status

```bash
docker-compose ps
```

**Expected output:**
```
Name                      Command               State           Ports
---------------------------------------------------------------------------------
law-analyse-backend    uvicorn app.main:app ...   Up      0.0.0.0:8000->8000/tcp
law-analyse-db         docker-entrypoint.sh ...   Up      0.0.0.0:5432->5432/tcp
law-analyse-frontend   docker-entrypoint.sh ...   Up      0.0.0.0:4321->4321/tcp
```

All services should show **State: Up**

---

## Step 5: Run Database Migrations

```bash
docker-compose exec backend alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> abc123, initial migration
```

---

## Step 6: Access the Application

### Frontend (User Interface)
```
http://localhost:4321
```

### Backend API Documentation
```
http://localhost:8000/docs
```

### Database (PostgreSQL)
```
Host: localhost
Port: 5432
Database: law_analyse
User: lawanalyse
Password: lawanalyse_local_password_2026
```

---

## Step 7: Test the Application

### Via API Documentation (Swagger UI)

1. Open: http://localhost:8000/docs
2. Try the `/laws` endpoint:
   - Click "GET /laws"
   - Click "Try it out"
   - Click "Execute"
   - Should return empty array `[]`

### Via Frontend

1. Open: http://localhost:4321
2. You should see the Law Analyse homepage
3. Try uploading a PDF law document

---

## Useful Commands

### View Logs

**All services:**
```bash
docker-compose logs -f
```

**Backend only:**
```bash
docker-compose logs -f backend
```

**Frontend only:**
```bash
docker-compose logs -f frontend
```

**Database only:**
```bash
docker-compose logs -f db
```

### Stop Services

```bash
docker-compose stop
```

### Start Services (after stop)

```bash
docker-compose start
```

### Restart Services

```bash
docker-compose restart
```

### Stop and Remove Everything

```bash
docker-compose down
```

**Remove everything including database data:**
```bash
docker-compose down -v
```

### Rebuild Images (after code changes)

```bash
docker-compose up -d --build
```

---

## Troubleshooting

### Problem: "Couldn't connect to Docker daemon"

**Solution:** Start Docker Desktop
```bash
"C:\Program Files\Docker\Docker\Docker Desktop.exe"
```
Wait 30-60 seconds for Docker to fully start.

### Problem: "Port 5432 is already in use"

**Solution:** Stop local PostgreSQL or change port in docker-compose.yml
```yaml
ports:
  - "5433:5432"  # Use port 5433 instead
```

### Problem: "Port 8000 is already in use"

**Solution:** Stop other services on port 8000 or change port
```yaml
ports:
  - "8001:8000"  # Use port 8001 instead
```

### Problem: Backend shows "Connection refused" to database

**Solution:** Wait a bit longer for database to start, then restart backend
```bash
docker-compose restart backend
```

### Problem: "OPENAI_API_KEY not set"

**Solution:** Edit `.env` file and add your API key
```bash
notepad .env
```

### Problem: Frontend can't connect to backend

**Solution:** Check backend is running
```bash
docker-compose ps backend
curl http://localhost:8000/docs
```

---

## Development Workflow

### Make Code Changes

1. Edit code in `backend/` or `frontend/`
2. Rebuild and restart:
   ```bash
   docker-compose up -d --build
   ```

### View Real-time Logs

```bash
docker-compose logs -f backend frontend
```

### Access Database

```bash
docker-compose exec db psql -U lawanalyse -d law_analyse
```

**Useful SQL commands:**
```sql
-- List tables
\dt

-- View laws
SELECT * FROM laws;

-- View articles
SELECT * FROM articles LIMIT 10;

-- Exit
\q
```

---

## Performance Tips

### Speed Up Builds

Add to `.dockerignore` in backend and frontend:
```
node_modules
.venv
__pycache__
*.pyc
.git
```

### Limit Resources

Edit `docker-compose.yml` to add resource limits:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

---

## Production Deployment

**Note:** This Docker setup is for local development.

For production deployment, see:
- `DEPLOYMENT.md` - Railway + Vercel + Neon
- `STEP_BY_STEP_DEPLOYMENT.md` - Detailed instructions

---

## URLs Summary

| Service | URL |
|---------|-----|
| Frontend | http://localhost:4321 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Database | localhost:5432 |

---

## Environment Variables

### Root `.env`
```bash
DB_PASSWORD=lawanalyse_local_password_2026
OPENAI_API_KEY=sk-proj-...
```

### `backend/.env`
```bash
DATABASE_URL=postgresql://lawanalyse:lawanalyse_local_password_2026@localhost:5432/law_analyse
OPENAI_API_KEY=sk-proj-...
PORT=8000
HOST=0.0.0.0
CORS_ORIGINS=http://localhost:4321,http://localhost:3000
ENVIRONMENT=development
```

---

## Next Steps

1. ✅ Start Docker Desktop
2. ✅ Configure `.env` with OpenAI API key
3. ✅ Run `docker-compose up -d`
4. ✅ Run migrations
5. ✅ Access http://localhost:4321
6. ✅ Test with a law PDF

---

**Happy coding!** 🚀

For issues, see: https://github.com/nposeo/law-analyse/issues
