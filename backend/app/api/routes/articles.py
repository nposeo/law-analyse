"""API routes for articles."""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.db_service import DatabaseService
from app.models.schemas import ArticleResponse

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/law/{law_id}", response_model=List[ArticleResponse])
async def get_articles_by_law(
    law_id: UUID,
    db: Session = Depends(get_db)
):
    """Get all articles for a law."""
    db_service = DatabaseService(db)

    # Verify law exists
    law = db_service.get_law(law_id)
    if not law:
        raise HTTPException(status_code=404, detail="Law not found")

    articles = db_service.get_articles_by_law(law_id)
    return articles


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: UUID,
    db: Session = Depends(get_db)
):
    """Get article by ID with norms."""
    db_service = DatabaseService(db)
    article = db_service.get_article_with_norms(article_id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return article
