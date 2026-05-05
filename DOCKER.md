# Docker Deployment Guide

## Quick Start with Docker Compose

### 1. Prerequisites

- Docker Desktop installed
- OpenAI API key

### 2. Setup Environment

Create `.env` file in project root:

```env
DB_PASSWORD=your_secure_password
OPENAI_API_KEY=sk-your-openai-key-here
```

### 3. Start All Services

```bash
# Build and start all containers
docker-compose up -d

# Check logs
docker-compose logs -f

# Check status
docker-compose ps
```

Services will be available at:
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Frontend:** http://localhost:4321
- **PostgreSQL:** localhost:5432

### 4. Run Migrations

```bash
# Run migrations inside backend container
docker-compose exec backend alembic upgrade head
```

### 5. Test the Application

```bash
# Health check
curl http://localhost:8000/health

# Create a law
curl -X POST http://localhost:8000/laws/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Law"}'
```

### 6. Stop Services

```bash
# Stop all containers
docker-compose down

# Stop and remove volumes (WARNING: deletes database)
docker-compose down -v
```

## Individual Container Commands

### Backend Only

```bash
# Build backend image
docker build -t law-analyse-backend ./backend

# Run backend container
docker run -d \
  --name law-analyse-backend \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e OPENAI_API_KEY="sk-..." \
  law-analyse-backend
```

### Frontend Only

```bash
# Build frontend image
docker build -t law-analyse-frontend ./frontend

# Run frontend container
docker run -d \
  --name law-analyse-frontend \
  -p 4321:4321 \
  -e PUBLIC_API_URL="http://localhost:8000" \
  law-analyse-frontend
```

### PostgreSQL Only

```bash
# Run PostgreSQL container
docker run -d \
  --name law-analyse-db \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=law_analyse \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:15-alpine
```

## Production Deployment

For production, we recommend:

1. **Database:** Neon PostgreSQL (managed)
2. **Backend:** Railway or Render (with Dockerfile)
3. **Frontend:** Vercel (better performance than Docker)

See `DEPLOYMENT.md` for cloud deployment instructions.

## Troubleshooting

### Backend can't connect to database

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Verify connection string
docker-compose exec backend env | grep DATABASE_URL
```

### Frontend can't reach backend

```bash
# Check backend is running
curl http://localhost:8000/health

# Check CORS settings in backend/app/main.py
# Should include: http://localhost:4321
```

### Migrations fail

```bash
# Check database connection
docker-compose exec backend psql $DATABASE_URL -c "SELECT 1"

# Reset migrations (WARNING: deletes data)
docker-compose down -v
docker-compose up -d db
docker-compose exec backend alembic upgrade head
```

### Out of disk space

```bash
# Clean up unused Docker resources
docker system prune -a

# Remove old volumes
docker volume prune
```

## Development with Docker

For development, you can mount local code:

```yaml
# Add to docker-compose.yml backend service:
volumes:
  - ./backend:/app
  - /app/.venv  # Exclude venv

# Add to frontend service:
volumes:
  - ./frontend:/app
  - /app/node_modules  # Exclude node_modules
```

Then restart:
```bash
docker-compose up -d
```

Changes will be reflected immediately with hot reload.

## Monitoring

### View logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Resource usage

```bash
# Container stats
docker stats

# Disk usage
docker system df
```

### Database backup

```bash
# Backup
docker-compose exec db pg_dump -U lawanalyse law_analyse > backup.sql

# Restore
docker-compose exec -T db psql -U lawanalyse law_analyse < backup.sql
```

## Security Notes

- Change default passwords in production
- Use secrets management (Docker secrets, env files)
- Don't commit `.env` files to git
- Use HTTPS in production (reverse proxy like Nginx)
- Limit database access to backend only
- Regular security updates: `docker-compose pull`
