"""API routes for processing laws."""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.db_service import DatabaseService
from app.services.pdf_parser import parse_law_pdf
from app.services.ai_extractor import extract_norm_from_article
from app.models.database import ProcessingStatus
from app.models.schemas import ProcessingStatusResponse, ArticleCreate, NormCreate

router = APIRouter(prefix="/process", tags=["processing"])


async def process_law_background(law_id: UUID, pdf_path: str, db: Session):
    """
    Background task to process a law PDF.

    Steps:
    1. Parse PDF to extract articles
    2. For each article, run AI extraction
    3. Save articles and norms to database
    4. Update law status
    """
    db_service = DatabaseService(db)

    try:
        # Update status to processing
        db_service.update_law_status(law_id, ProcessingStatus.PROCESSING)

        # Step 1: Parse PDF
        articles = parse_law_pdf(pdf_path)

        # Step 2 & 3: Process each article
        for parsed_article in articles:
            # Create article record
            article_data = ArticleCreate(
                law_id=law_id,
                article_number=parsed_article.article_number,
                title=parsed_article.title,
                full_text=parsed_article.full_text,
                hierarchy_path=parsed_article.hierarchy_path
            )
            article = db_service.create_article(article_data)

            # Extract norm with AI
            try:
                norm_data = extract_norm_from_article(
                    article_text=parsed_article.full_text,
                    article_id=parsed_article.article_number,
                    title=parsed_article.title
                )

                # Create norm record
                norm_create = NormCreate(
                    article_id=article.id,
                    norm_text=norm_data["norm"],
                    subject=norm_data["subject"],
                    simplified_explanation=norm_data["simplified_explanation"],
                    confidence_score=norm_data["confidence_score"],
                    needs_human_review=norm_data["needs_human_review"],
                    extraction_metadata=norm_data.get("extraction_metadata")
                )
                db_service.create_norm(norm_create)

            except Exception as e:
                # Log error but continue processing other articles
                print(f"Error extracting norm for article {parsed_article.article_number}: {e}")

        # Update status to completed
        db_service.update_law_status(law_id, ProcessingStatus.COMPLETED)

    except Exception as e:
        # Update status to failed
        db_service.update_law_status(law_id, ProcessingStatus.FAILED)
        print(f"Error processing law {law_id}: {e}")


@router.post("/{law_id}", response_model=ProcessingStatusResponse)
async def trigger_processing(
    law_id: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Trigger processing of a law PDF.

    This starts a background task that:
    1. Parses the PDF
    2. Extracts articles
    3. Runs AI extraction on each article
    4. Saves results to database
    """
    db_service = DatabaseService(db)

    # Get law
    law = db_service.get_law(law_id)
    if not law:
        raise HTTPException(status_code=404, detail="Law not found")

    if not law.pdf_url:
        raise HTTPException(status_code=400, detail="Law has no PDF file")

    # Check if already processing
    if law.processing_status == ProcessingStatus.PROCESSING:
        raise HTTPException(status_code=400, detail="Law is already being processed")

    # Add background task
    background_tasks.add_task(process_law_background, law_id, law.pdf_url, db)

    return ProcessingStatusResponse(
        law_id=law_id,
        status=ProcessingStatus.PROCESSING.value,
        message="Processing started"
    )


@router.get("/{law_id}/status", response_model=ProcessingStatusResponse)
async def get_processing_status(
    law_id: UUID,
    db: Session = Depends(get_db)
):
    """Get processing status for a law."""
    db_service = DatabaseService(db)

    law = db_service.get_law(law_id)
    if not law:
        raise HTTPException(status_code=404, detail="Law not found")

    # Calculate progress if processing
    progress = None
    if law.processing_status == ProcessingStatus.PROCESSING:
        articles = db_service.get_articles_by_law(law_id)
        # Rough estimate based on articles created
        progress = len(articles) * 2.5  # Assuming ~40 articles total

    return ProcessingStatusResponse(
        law_id=law_id,
        status=law.processing_status.value,
        progress=progress,
        message=f"Status: {law.processing_status.value}"
    )
