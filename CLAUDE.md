# Law Analyse Project Rules

## Legal Accuracy
- Ukrainian law text is the source of truth. Never invent legal interpretations.
- If LLM confidence < 0.8, mark `needs_human_review=true`. Do not guess.
- Simplified explanations must preserve legal precision. Avoid oversimplification that changes meaning.

## Code Standards
- Backend: Use type hints (Python 3.11+), async/await for I/O
- Frontend: TypeScript strict mode, no `any` types
- All API responses must match Pydantic schemas
- Database queries use SQLAlchemy ORM (no raw SQL)

## Testing
- Test PDF parser with real Ukrainian legal documents
- Compare adversarial review vs single-pass extraction accuracy
- Verify JSON Schema validation catches malformed outputs

## Security
- Never commit `.env` files
- Validate all file uploads (PDF only, max 50MB)
- Sanitize user inputs in search queries
- Use parameterized database queries

## Git Workflow
- Commit messages in English
- Branch naming: `feature/`, `fix/`, `docs/`
- No force push to main

## MVP Configuration
- LLM: OpenAI GPT-4o
- Test Law: Закон України "Про освіту"
- Adversarial Review: 2-agent chain (Generator → Critic/Finalizer)
- Deployment: Vercel (frontend) + Railway (backend) + Neon PostgreSQL
