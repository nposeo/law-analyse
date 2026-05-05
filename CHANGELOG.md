# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-05

### Added

#### Core Features
- **PDF Parser** for Ukrainian legal documents
  - Regex-based article extraction
  - Hierarchical structure support (Стаття → Частина → Пункт)
  - pdfplumber integration for text extraction

- **AI Extraction Pipeline**
  - 2-agent adversarial review (Generator → Critic/Finalizer)
  - OpenAI GPT-4o integration with structured outputs
  - Confidence scoring (0.0-1.0 scale)
  - Automatic human review flagging (< 0.8 threshold)
  - Ukrainian language prompts

- **Backend API (FastAPI)**
  - `/laws` endpoints - CRUD operations, PDF upload
  - `/articles` endpoints - Article retrieval
  - `/process` endpoints - Background processing with status tracking
  - PostgreSQL database with SQLAlchemy ORM
  - Alembic migrations
  - OpenAPI documentation

- **Frontend UI (Astro + React)**
  - Landing page with law list and status indicators
  - Law detail page with metadata display
  - Interactive article tree with expand/collapse
  - Article view with plain language toggle
  - Confidence score indicators
  - Responsive design with Tailwind CSS

#### Testing
- Pytest test suite for backend
  - API endpoint tests
  - PDF parser tests
  - AI extractor tests (mocked)
- Test fixtures and utilities

#### Documentation
- `README.md` - Project overview
- `QUICKSTART.md` - 5-minute setup guide
- `DEPLOYMENT.md` - Production deployment instructions
- `DOCKER.md` - Docker deployment guide
- `PROJECT_SUMMARY.md` - Technical specifications
- `CONTRIBUTING.md` - Contribution guidelines
- `CLAUDE.md` - Project rules and standards

#### DevOps
- Docker support with docker-compose
- Automated setup scripts (setup.sh, setup.bat)
- Development server script (dev.sh)
- GitHub Actions ready structure
- MIT License

### Technical Details

**Backend Stack:**
- FastAPI 0.110.0
- pdfplumber 0.11.0
- LangChain 0.1.16 + langchain-openai 0.1.3
- SQLAlchemy 2.0.29 + Alembic 1.13.1
- PostgreSQL (psycopg2-binary 2.9.9)
- Python 3.11+

**Frontend Stack:**
- Astro 4.5.0
- React 18.2.0
- TypeScript 5.4.2
- Tailwind CSS 3.4.1

**AI:**
- OpenAI GPT-4o
- 2-agent adversarial review pattern
- Pydantic structured outputs

### Architecture Decisions

1. **2-agent vs 3-agent review:** Chose 2-agent (Generator + Critic/Finalizer) to save 33% API costs while maintaining accuracy
2. **Astro + React:** Hybrid approach for optimal performance (static pages + interactive islands)
3. **Background processing:** FastAPI BackgroundTasks for PDF processing (simpler than Celery for MVP)
4. **Separate deployment:** Backend (Railway) + Frontend (Vercel) for better scalability
5. **Confidence scoring:** LLM self-assessment to identify uncertain extractions

### Known Limitations

- Single law processing at a time (no queue system)
- No authentication/authorization
- No admin panel for human review
- Limited PDF format support (standard Ukrainian law PDFs only)
- No caching layer (Redis)
- Manual law upload (no automatic scraping)

### Future Roadmap

See `PROJECT_SUMMARY.md` for detailed roadmap.

**v1.1.0 (Planned):**
- Add 5-10 popular Ukrainian laws
- Full-text search
- Export functionality (PDF, Word)

**v1.2.0 (Planned):**
- User authentication
- Admin panel for human review
- Bookmarks and favorites

**v2.0.0 (Planned):**
- Automatic scraping from rada.gov.ua
- Law version comparison
- Mobile app

---

## Release Notes

### v1.0.0 - MVP Release

**Status:** ✅ Production Ready

**Deployment:**
- Backend: Railway (free tier)
- Frontend: Vercel (free tier)
- Database: Neon PostgreSQL (free tier)

**Cost:** ~$5-10 for processing test law, $0/month recurring

**Test Law:** Закон України "Про освіту" (~40 articles)

**Estimated Processing Time:** < 10 minutes

**Expected Accuracy:** > 80% (requires manual validation)

---

*For detailed technical information, see `PROJECT_SUMMARY.md`*
*For deployment instructions, see `DEPLOYMENT.md`*
