# Law Analyse MVP

AI-powered application for structuring and analyzing Ukrainian laws.

## Features

- 📄 PDF parsing of Ukrainian legal documents
- 🤖 AI extraction with adversarial review (2-agent chain)
- 🌳 Interactive article tree navigation
- 💬 Plain language explanations
- ⚠️ Confidence scoring with human review flags

## Tech Stack

**Backend:**
- FastAPI + Python 3.11
- pdfplumber for PDF parsing
- LangChain + OpenAI GPT-4o for AI extraction
- PostgreSQL + SQLAlchemy

**Frontend:**
- Astro + React + TypeScript
- Tailwind CSS

**Deployment:**
- Frontend: Vercel
- Backend: Railway
- Database: Neon PostgreSQL

## Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL and OPENAI_API_KEY

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
law-analyse/
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── services/ # Business logic (PDF, AI)
│   │   ├── models/   # Database models
│   │   └── core/     # Config, prompts
│   └── tests/
├── frontend/         # Astro + React application
│   └── src/
│       ├── pages/    # Astro pages
│       ├── components/ # React components
│       └── lib/      # API client
└── CLAUDE.md         # Project rules
```

## Test Law

MVP uses **Закон України "Про освіту"** (~40 articles) for testing.

## License

MIT
