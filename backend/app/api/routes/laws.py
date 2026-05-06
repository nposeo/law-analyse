"""API routes for laws."""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.db_service import DatabaseService
from app.models.schemas import LawCreate, LawResponse, LawDetailResponse

router = APIRouter(prefix="/laws", tags=["laws"])


@router.post("/", response_model=LawResponse, status_code=201)
async def create_law(
    law_data: LawCreate,
    db: Session = Depends(get_db)
):
    """Create a new law."""
    try:
        db_service = DatabaseService(db)
        law = db_service.create_law(law_data)
        return law
    except Exception as e:
        import traceback
        print(f"Error creating law: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create law: {str(e)}")


@router.get("/", response_model=List[LawResponse])
async def get_all_laws(db: Session = Depends(get_db)):
    """Get all laws."""
    db_service = DatabaseService(db)
    laws = db_service.get_all_laws()
    return laws


@router.get("/{law_id}", response_model=LawDetailResponse)
async def get_law(law_id: UUID, db: Session = Depends(get_db)):
    """Get law by ID with all articles and norms."""
    db_service = DatabaseService(db)
    law = db_service.get_law_with_articles(law_id)

    if not law:
        raise HTTPException(status_code=404, detail="Law not found")

    return law


@router.post("/upload", response_model=LawResponse)
async def upload_law_pdf(
    file: UploadFile = File(...),
    title: str = "",
    db: Session = Depends(get_db)
):
    """
    Upload a law PDF file.

    For MVP, this creates a law record and saves the file.
    Processing is triggered separately via /process endpoint.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        # For MVP, we'll store the file path
        # In production, upload to cloud storage (S3, etc.)
        import os
        from pathlib import Path

        # Use /app/uploads for Railway volume, fallback to local uploads/
        if os.path.exists("/app"):
            upload_dir = Path("/app/uploads")
        else:
            upload_dir = Path("uploads").absolute()

        upload_dir.mkdir(exist_ok=True, parents=True)

        file_path = upload_dir / file.filename

        # Save file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        print(f"File saved to: {file_path}")
        print(f"File exists: {file_path.exists()}")
        print(f"File size: {file_path.stat().st_size if file_path.exists() else 0}")

        # Create law record
        db_service = DatabaseService(db)
        law_data = LawCreate(
            title=title or file.filename,
            pdf_url=str(file_path)  # Store full absolute path
        )
        law = db_service.create_law(law_data)

        return law
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Error uploading law: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to upload law: {str(e)}")
