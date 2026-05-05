"""Database models for Law Analyse."""
import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Text, DateTime, Float, Boolean, ForeignKey, Enum, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class ProcessingStatus(str, PyEnum):
    """Law processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Law(Base):
    """Law document model."""
    __tablename__ = "laws"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    document_number = Column(String(100))
    publication_date = Column(DateTime)
    issuing_body = Column(String(255))
    pdf_url = Column(Text)
    processing_status = Column(
        Enum(ProcessingStatus),
        default=ProcessingStatus.PENDING,
        nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    articles = relationship("Article", back_populates="law", cascade="all, delete-orphan")


class Article(Base):
    """Article model with hierarchical structure."""
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    law_id = Column(UUID(as_uuid=True), ForeignKey("laws.id"), nullable=False)
    article_number = Column(String(50), nullable=False)
    title = Column(Text)
    full_text = Column(Text, nullable=False)
    hierarchy_path = Column(ARRAY(String))  # ['1', '1.1', '1.1.a']

    # Relationships
    law = relationship("Law", back_populates="articles")
    norms = relationship("Norm", back_populates="article", cascade="all, delete-orphan")


class Norm(Base):
    """AI-extracted norm from article."""
    __tablename__ = "norms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id"), nullable=False)
    norm_type = Column(String(50))  # 'obligation', 'prohibition', 'right', 'definition'
    norm_text = Column(Text, nullable=False)
    subject = Column(Text)
    simplified_explanation = Column(Text)
    confidence_score = Column(Float, nullable=False)
    needs_human_review = Column(Boolean, default=False, nullable=False)
    extraction_metadata = Column(JSONB)  # LLM model, timestamp, review chain

    # Relationships
    article = relationship("Article", back_populates="norms")
