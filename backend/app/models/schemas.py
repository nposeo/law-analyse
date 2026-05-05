"""Pydantic schemas for API validation."""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


class NormExtraction(BaseModel):
    """Schema for AI-extracted norm (used with LLM structured output)."""
    article_id: str
    title: str
    norm: str = Field(description="Що регулюється цією статтею")
    subject: str = Field(description="На кого поширюється")
    simplified_explanation: str = Field(description="Пояснення простою мовою")
    confidence_score: float = Field(ge=0.0, le=1.0)
    needs_human_review: bool = Field(default=False)


class NormCreate(BaseModel):
    """Schema for creating a norm."""
    article_id: UUID
    norm_type: Optional[str] = None
    norm_text: str
    subject: str
    simplified_explanation: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    needs_human_review: bool = False
    extraction_metadata: Optional[dict] = None


class NormResponse(BaseModel):
    """Schema for norm response."""
    id: UUID
    article_id: UUID
    norm_type: Optional[str]
    norm_text: str
    subject: str
    simplified_explanation: str
    confidence_score: float
    needs_human_review: bool
    extraction_metadata: Optional[dict]

    class Config:
        from_attributes = True


class ArticleCreate(BaseModel):
    """Schema for creating an article."""
    law_id: UUID
    article_number: str
    title: Optional[str] = None
    full_text: str
    hierarchy_path: Optional[list[str]] = None


class ArticleResponse(BaseModel):
    """Schema for article response."""
    id: UUID
    law_id: UUID
    article_number: str
    title: Optional[str]
    full_text: str
    hierarchy_path: Optional[list[str]]
    norms: list[NormResponse] = []

    class Config:
        from_attributes = True


class LawCreate(BaseModel):
    """Schema for creating a law."""
    title: str
    document_number: Optional[str] = None
    publication_date: Optional[datetime] = None
    issuing_body: Optional[str] = None
    pdf_url: Optional[str] = None


class LawResponse(BaseModel):
    """Schema for law response."""
    id: UUID
    title: str
    document_number: Optional[str]
    publication_date: Optional[datetime]
    issuing_body: Optional[str]
    pdf_url: Optional[str]
    processing_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class LawDetailResponse(LawResponse):
    """Schema for detailed law response with articles."""
    articles: list[ArticleResponse] = []


class ProcessingStatusResponse(BaseModel):
    """Schema for processing status response."""
    law_id: UUID
    status: str
    progress: Optional[float] = None
    message: Optional[str] = None
