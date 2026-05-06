from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.routes import laws, articles, process

settings = get_settings()

app = FastAPI(
    title="Law Analyse API",
    description="API for analyzing Ukrainian laws with AI",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(laws.router)
app.include_router(articles.router)
app.include_router(process.router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Law Analyse API",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "environment": settings.environment
    }


@app.get("/debug/paths")
async def debug_paths():
    """Debug endpoint to check paths on Railway."""
    import os
    from pathlib import Path

    return {
        "cwd": os.getcwd(),
        "app_exists": os.path.exists("/app"),
        "app_uploads_exists": os.path.exists("/app/uploads"),
        "uploads_exists": os.path.exists("uploads"),
        "uploads_absolute": str(Path("uploads").absolute()),
        "env_vars": {
            "PORT": os.getenv("PORT"),
            "DATABASE_URL": "***" if os.getenv("DATABASE_URL") else None
        }
    }
