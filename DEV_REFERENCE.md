# 🚀 Law Analyse - Developer Quick Reference

## Quick Commands

### Development

```bash
# Setup (first time)
./setup.sh          # Linux/Mac
setup.bat           # Windows

# Start development servers
./dev.sh            # Linux/Mac
dev.bat             # Windows

# Backend only
cd backend
source .venv/bin/activate  # Linux/Mac: .venv\Scripts\activate
uvicorn app.main:app --reload

# Frontend only
cd frontend
npm run dev

# Run tests
cd backend
pytest

# Docker
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Database

```bash
# Create migration
cd backend
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Reset database
alembic downgrade base
alembic upgrade head
```

### Git

```bash
# Commit
git add .
git commit -m "type: description"

# Push
git push origin main

# Create branch
git checkout -b feature/name

# Merge
git checkout main
git merge feature/name
```

## Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/lawanalyse

# OpenAI
OPENAI_API_KEY=sk-...

# Server
PORT=8000
HOST=0.0.0.0

# CORS
CORS_ORIGINS=http://localhost:4321,http://localhost:3000
```

### Frontend (.env)

```bash
# API URL
PUBLIC_API_URL=http://localhost:8000

# Environment
PUBLIC_ENV=development
```

## API Endpoints

### Laws

```bash
# Upload PDF
curl -X POST "http://localhost:8000/laws/upload" \
  -F "file=@law.pdf" \
  -F "title=Закон України про освіту" \
  -F "document_number=2145-VIII" \
  -F "publication_date=2017-09-05"

# List laws
curl "http://localhost:8000/laws"

# Get law
curl "http://localhost:8000/laws/{id}"

# Delete law
curl -X DELETE "http://localhost:8000/laws/{id}"
```

### Articles

```bash
# Get articles
curl "http://localhost:8000/laws/{law_id}/articles"

# Get article
curl "http://localhost:8000/articles/{id}"

# Get norms
curl "http://localhost:8000/articles/{id}/norms"
```

### Processing

```bash
# Start processing
curl -X POST "http://localhost:8000/process/{law_id}"

# Check status
curl "http://localhost:8000/process/{law_id}/status"
```

## Project Structure

```
law-analyse/
├── backend/
│   ├── app/
│   │   ├── api/routes/      # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── models/          # Database models
│   │   ├── core/            # Config, prompts
│   │   └── main.py          # FastAPI app
│   ├── tests/               # Pytest tests
│   ├── migrations/          # Alembic migrations
│   └── requirements.txt     # Dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/           # Astro pages
│   │   ├── components/      # React components
│   │   └── lib/             # API client
│   └── package.json         # Dependencies
└── docker-compose.yml       # Docker config
```

## Common Tasks

### Add New API Endpoint

1. Create route in `backend/app/api/routes/`
2. Add business logic in `backend/app/services/`
3. Update Pydantic schemas in `backend/app/models/schemas.py`
4. Write tests in `backend/tests/`
5. Update API documentation

### Add New Frontend Component

1. Create component in `frontend/src/components/`
2. Import in page: `frontend/src/pages/`
3. Add TypeScript types
4. Style with Tailwind CSS
5. Test in browser

### Add New Database Model

1. Update `backend/app/models/database.py`
2. Create migration: `alembic revision --autogenerate -m "add model"`
3. Review migration in `backend/migrations/versions/`
4. Apply: `alembic upgrade head`
5. Update Pydantic schemas

### Update AI Prompts

1. Edit `backend/app/core/prompts.py`
2. Test with sample articles
3. Measure accuracy improvement
4. Document changes in CHANGELOG.md

## Debugging

### Backend

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Logging
import logging
logger = logging.getLogger(__name__)
logger.info("Message")
logger.error("Error", exc_info=True)

# FastAPI debug mode
uvicorn app.main:app --reload --log-level debug
```

### Frontend

```typescript
// Console logging
console.log('Debug:', data);
console.error('Error:', error);

// React DevTools
// Install browser extension

// Astro debug
npm run dev -- --verbose
```

### Database

```sql
-- Connect to PostgreSQL
psql -U user -d lawanalyse

-- List tables
\dt

-- Describe table
\d laws

-- Query
SELECT * FROM laws LIMIT 10;

-- Check migrations
SELECT * FROM alembic_version;
```

## Testing

### Backend Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_api.py::test_upload_law

# Run with coverage
pytest --cov=app --cov-report=html

# Run with verbose output
pytest -v

# Run only failed tests
pytest --lf
```

### Frontend Tests

```bash
# Run tests (if configured)
npm test

# Type check
npm run check

# Lint
npm run lint

# Build
npm run build
```

## Performance

### Backend Optimization

```python
# Use async/await
async def get_law(law_id: str):
    return await db.query(Law).filter(Law.id == law_id).first()

# Cache results
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_operation():
    pass

# Background tasks
from fastapi import BackgroundTasks

@app.post("/process/{law_id}")
async def process_law(law_id: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_pdf, law_id)
    return {"status": "processing"}
```

### Frontend Optimization

```typescript
// Lazy loading
const Component = lazy(() => import('./Component'));

// Memoization
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);

// Debouncing
const debouncedSearch = debounce(search, 300);
```

## Security

### Backend

```python
# Input validation
from pydantic import BaseModel, validator

class LawCreate(BaseModel):
    title: str
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v

# SQL injection prevention (SQLAlchemy)
# ✅ Good
db.query(Law).filter(Law.id == law_id).first()

# ❌ Bad
db.execute(f"SELECT * FROM laws WHERE id = '{law_id}'")

# File upload validation
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

### Frontend

```typescript
// XSS prevention (React auto-escapes)
// ✅ Good
<div>{userInput}</div>

// ❌ Bad
<div dangerouslySetInnerHTML={{__html: userInput}} />

// API calls with error handling
try {
  const response = await fetch(url);
  if (!response.ok) throw new Error('API error');
  const data = await response.json();
} catch (error) {
  console.error('Error:', error);
}
```

## Deployment

### Railway (Backend)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up

# View logs
railway logs
```

### Vercel (Frontend)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Production
vercel --prod
```

### Neon (Database)

```bash
# Get connection string from Neon dashboard
# Add to Railway environment variables:
DATABASE_URL=postgresql://user:password@host/db

# Run migrations
railway run alembic upgrade head
```

## Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'app'`
```bash
# Solution: Activate virtual environment
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

**Issue:** `CORS error in frontend`
```python
# Solution: Update CORS_ORIGINS in backend/.env
CORS_ORIGINS=http://localhost:4321
```

**Issue:** `Database connection failed`
```bash
# Solution: Check PostgreSQL is running
# Windows: Check Services
# Linux: sudo systemctl status postgresql
# Mac: brew services list
```

**Issue:** `OpenAI API error`
```bash
# Solution: Check API key in backend/.env
OPENAI_API_KEY=sk-...
# Verify key at: https://platform.openai.com/api-keys
```

**Issue:** `Port already in use`
```bash
# Solution: Kill process on port
# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## Useful Links

### Documentation
- FastAPI: https://fastapi.tiangolo.com
- Astro: https://docs.astro.build
- React: https://react.dev
- LangChain: https://python.langchain.com
- SQLAlchemy: https://docs.sqlalchemy.org
- Alembic: https://alembic.sqlalchemy.org

### Tools
- OpenAPI Docs: http://localhost:8000/docs
- PostgreSQL Admin: https://www.pgadmin.org
- Postman: https://www.postman.com
- Docker Desktop: https://www.docker.com/products/docker-desktop

### Community
- GitHub Issues: https://github.com/nposeo/law-analyse/issues
- GitHub Discussions: https://github.com/nposeo/law-analyse/discussions

## Commit Message Convention

```
type(scope): description

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Tests
- chore: Maintenance

Examples:
feat(api): add law export endpoint
fix(parser): handle articles without titles
docs(readme): update installation instructions
test(api): add tests for article endpoints
```

## Code Style

### Python (Black + isort)

```bash
# Format code
black .
isort .

# Check
black --check .
isort --check .
```

### TypeScript (Prettier)

```bash
# Format code
npm run format

# Check
npm run format:check
```

## Monitoring

### Backend Logs

```bash
# Development
uvicorn app.main:app --reload --log-level debug

# Production (Railway)
railway logs
```

### Frontend Logs

```bash
# Development
npm run dev

# Production (Vercel)
vercel logs
```

### Database Monitoring

```sql
-- Active connections
SELECT * FROM pg_stat_activity;

-- Table sizes
SELECT 
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

**Last Updated:** 2026-05-05  
**Version:** 1.0.0  
**Maintainer:** nposeo
