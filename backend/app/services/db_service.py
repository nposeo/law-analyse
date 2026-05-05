"""Database service for CRUD operations."""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from app.models.database import Law, Article, Norm, ProcessingStatus
from app.models.schemas import LawCreate, ArticleCreate, NormCreate


class DatabaseService:
    """Service for database operations."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    # Law operations
    def create_law(self, law_data: LawCreate) -> Law:
        """Create a new law."""
        law = Law(**law_data.dict())
        self.db.add(law)
        self.db.commit()
        self.db.refresh(law)
        return law

    def get_law(self, law_id: UUID) -> Optional[Law]:
        """Get law by ID."""
        return self.db.query(Law).filter(Law.id == law_id).first()

    def get_law_with_articles(self, law_id: UUID) -> Optional[Law]:
        """Get law with all articles and norms."""
        return (
            self.db.query(Law)
            .options(
                joinedload(Law.articles).joinedload(Article.norms)
            )
            .filter(Law.id == law_id)
            .first()
        )

    def get_all_laws(self) -> List[Law]:
        """Get all laws."""
        return self.db.query(Law).all()

    def update_law_status(self, law_id: UUID, status: ProcessingStatus) -> Optional[Law]:
        """Update law processing status."""
        law = self.get_law(law_id)
        if law:
            law.processing_status = status
            self.db.commit()
            self.db.refresh(law)
        return law

    # Article operations
    def create_article(self, article_data: ArticleCreate) -> Article:
        """Create a new article."""
        article = Article(**article_data.dict())
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        return article

    def get_article(self, article_id: UUID) -> Optional[Article]:
        """Get article by ID."""
        return self.db.query(Article).filter(Article.id == article_id).first()

    def get_articles_by_law(self, law_id: UUID) -> List[Article]:
        """Get all articles for a law."""
        return (
            self.db.query(Article)
            .filter(Article.law_id == law_id)
            .order_by(Article.article_number)
            .all()
        )

    def get_article_with_norms(self, article_id: UUID) -> Optional[Article]:
        """Get article with all norms."""
        return (
            self.db.query(Article)
            .options(joinedload(Article.norms))
            .filter(Article.id == article_id)
            .first()
        )

    # Norm operations
    def create_norm(self, norm_data: NormCreate) -> Norm:
        """Create a new norm."""
        norm = Norm(**norm_data.dict())
        self.db.add(norm)
        self.db.commit()
        self.db.refresh(norm)
        return norm

    def get_norms_by_article(self, article_id: UUID) -> List[Norm]:
        """Get all norms for an article."""
        return self.db.query(Norm).filter(Norm.article_id == article_id).all()

    def get_norms_needing_review(self, law_id: UUID) -> List[Norm]:
        """Get all norms that need human review for a law."""
        return (
            self.db.query(Norm)
            .join(Article)
            .filter(Article.law_id == law_id)
            .filter(Norm.needs_human_review == True)
            .all()
        )
