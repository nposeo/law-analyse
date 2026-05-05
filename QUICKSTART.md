# Quick Start Guide - Law Analyse MVP

## Швидкий старт (5 хвилин)

### 1. Клонування та налаштування

```bash
# Якщо репозиторій вже на GitHub
git clone https://github.com/your-username/law-analyse.git
cd law-analyse

# Або використовуйте існуючу директорію
cd D:\server\OpenServer\domains\LawAnalyse\www
```

### 2. Backend Setup

```bash
cd backend

# Створити віртуальне середовище
python -m venv .venv

# Активувати (Windows)
.venv\Scripts\activate

# Активувати (Linux/Mac)
source .venv/bin/activate

# Встановити залежності
pip install -r requirements.txt

# Налаштувати .env
cp .env.example .env
```

**Відредагуйте `.env`:**
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/law_analyse
OPENAI_API_KEY=sk-your-openai-key-here
ENVIRONMENT=development
```

**Запустити PostgreSQL локально (Docker):**
```bash
docker run --name law-analyse-db \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=law_analyse \
  -p 5432:5432 \
  -d postgres:15
```

**Запустити міграції:**
```bash
alembic upgrade head
```

**Запустити сервер:**
```bash
uvicorn app.main:app --reload
```

Backend доступний на: http://localhost:8000

### 3. Frontend Setup

```bash
cd frontend

# Встановити залежності
npm install

# Створити .env
echo "PUBLIC_API_URL=http://localhost:8000" > .env

# Запустити dev server
npm run dev
```

Frontend доступний на: http://localhost:4321

### 4. Тестування API

**Перевірка здоров'я:**
```bash
curl http://localhost:8000/health
```

**Створити закон:**
```bash
curl -X POST http://localhost:8000/laws/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Закон України про освіту",
    "document_number": "2145-VIII",
    "issuing_body": "Верховна Рада України"
  }'
```

**Завантажити PDF (якщо є файл):**
```bash
curl -X POST http://localhost:8000/laws/upload \
  -F "file=@path/to/law.pdf" \
  -F "title=Закон про освіту"
```

**Запустити обробку:**
```bash
# Замініть {law_id} на ID з попереднього запиту
curl -X POST http://localhost:8000/process/{law_id}
```

**Перевірити статус:**
```bash
curl http://localhost:8000/process/{law_id}/status
```

### 5. Запуск тестів

```bash
cd backend

# Запустити всі тести
pytest

# Запустити з coverage
pytest --cov=app --cov-report=html

# Запустити конкретний тест
pytest app/tests/test_api.py -v
```

## Швидке створення GitHub репозиторію (без gh CLI)

### Варіант 1: Через веб-інтерфейс

1. Відкрийте https://github.com/new
2. Назва: `law-analyse`
3. Опис: `AI-powered Ukrainian law analysis platform`
4. Public
5. НЕ додавайте README, .gitignore, license (вони вже є)
6. Create repository

**Підключити локальний репозиторій:**
```bash
cd D:\server\OpenServer\domains\LawAnalyse\www
git remote add origin https://github.com/YOUR-USERNAME/law-analyse.git
git branch -M main
git push -u origin main
```

### Варіант 2: Через Git

```bash
# Якщо ще не ініціалізовано
git init
git add .
git commit -m "feat: initial Law Analyse MVP"

# Створіть репозиторій на GitHub через веб, потім:
git remote add origin https://github.com/YOUR-USERNAME/law-analyse.git
git push -u origin main
```

## Швидкий Deployment

### Railway (Backend)

1. https://railway.app → New Project → Deploy from GitHub
2. Виберіть `law-analyse`
3. Root Directory: `backend`
4. Add variables:
   - `DATABASE_URL` (з Neon)
   - `OPENAI_API_KEY`
   - `ENVIRONMENT=production`
5. Deploy

### Vercel (Frontend)

1. https://vercel.com → New Project
2. Import `law-analyse`
3. Framework: Astro
4. Root Directory: `frontend`
5. Environment: `PUBLIC_API_URL` (Railway URL)
6. Deploy

### Neon (Database)

1. https://neon.tech → New Project
2. Назва: `law-analyse-db`
3. Copy connection string
4. Paste в Railway `DATABASE_URL`

## Troubleshooting

### Backend не запускається
```bash
# Перевірити Python версію (потрібна 3.11+)
python --version

# Перевірити залежності
pip list | grep fastapi

# Перевірити .env
cat .env
```

### Frontend не підключається до backend
```bash
# Перевірити CORS в backend/app/main.py
# Має бути: allow_origins=["http://localhost:4321"]

# Перевірити .env у frontend
cat frontend/.env
```

### Database connection error
```bash
# Перевірити PostgreSQL запущений
docker ps | grep postgres

# Перевірити connection string
echo $DATABASE_URL
```

### OpenAI API error
```bash
# Перевірити API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

## Корисні команди

```bash
# Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Frontend  
cd frontend
npm run dev -- --port 4321

# Database migrations
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head

# Tests
cd backend
pytest -v
pytest --cov=app

# Git
git status
git log --oneline
git diff
```

## Наступні кроки

1. ✅ Локальне тестування
2. ✅ Створення GitHub репозиторію
3. ⏳ Deployment на Railway + Vercel
4. ⏳ Завантаження тестового закону
5. ⏳ Перевірка точності екстракції

Детальні інструкції: `DEPLOYMENT.md`
