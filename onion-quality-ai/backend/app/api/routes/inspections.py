"""Inspection and image ingestion endpoints."""

from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.schemas.inspection import (
    InspectionCreate,
    InspectionUpdate,
    InspectionResponse,
    InspectionDetailResponse,
)
from app.schemas.image import ImageResponse
from app.services.inspection_service import InspectionService
from app.services.image_service import ImageService

router = APIRouter(prefix="/inspections", tags=["inspections"])


@router.post(
    "",
    response_model=InspectionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new inspection session",
)
async def create_inspection(
    payload: InspectionCreate,
    db: AsyncSession = Depends(get_db),
) -> InspectionResponse:
    """Initialize an inspection record for an onion lot."""
    return await InspectionService.create_inspection(db, payload)


@router.get(
    "",
    response_model=List[InspectionResponse],
    summary="List inspections with pagination and filtering",
)
async def list_inspections(
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(50, ge=1, le=100, description="Maximum items to return"),
    lot_id: Optional[str] = Query(None, description="Filter by lot identifier"),
    db: AsyncSession = Depends(get_db),
) -> List[InspectionResponse]:
    """Retrieve inspections ordered by creation time descending."""
    return await InspectionService.list_inspections(
        db,
        skip=skip,
        limit=limit,
        lot_id=lot_id,
    )


@router.get(
    "/{inspection_id}",
    response_model=InspectionDetailResponse,
    summary="Get inspection details with related entities",
)
async def get_inspection(
    inspection_id: str,
    db: AsyncSession = Depends(get_db),
) -> InspectionDetailResponse:
    """Retrieve full details of an inspection including images, onion instances, grades, and reports."""
    inspection = await InspectionService.get_inspection(db, inspection_id, load_relations=True)
    if not inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inspection '{inspection_id}' not found",
        )
    return inspection


@router.patch(
    "/{inspection_id}",
    response_model=InspectionResponse,
    summary="Update an inspection session",
)
async def update_inspection(
    inspection_id: str,
    payload: InspectionUpdate,
    db: AsyncSession = Depends(get_db),
) -> InspectionResponse:
    """Update status or grading profile of an existing inspection session."""
    inspection = await InspectionService.get_inspection(db, inspection_id, load_relations=False)
    if not inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inspection '{inspection_id}' not found",
        )
    return await InspectionService.update_inspection(db, inspection, payload)


@router.post(
    "/{inspection_id}/images",
    response_model=ImageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload and evaluate an inspection image",
)
async def upload_inspection_image(
    inspection_id: str,
    file: UploadFile = File(..., description="Image file (JPEG, JPG, PNG)"),
    image_type: str = Form("capture", description="Capture type/angle (e.g. top_view, tray, single)"),
    db: AsyncSession = Depends(get_db),
) -> ImageResponse:
    """Upload a produce capture image, run automated quality gates, and persist metadata."""
    # 1. Verify inspection existence
    inspection = await InspectionService.get_inspection(db, inspection_id, load_relations=False)
    if not inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inspection '{inspection_id}' not found",
        )

    # 2. Validate file extension
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ImageService.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{ext}'. Supported formats: JPEG, JPG, PNG.",
        )

    # 3. Read content and validate file size
    settings = get_settings()
    max_bytes = settings.max_image_size_mb * 1024 * 1024
    content = await file.read()

    if len(content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size ({len(content) / (1024*1024):.1f} MB) exceeds maximum allowed limit of {settings.max_image_size_mb} MB.",
        )

    # 4. Process storage, quality evaluation, and database record
    try:
        return await ImageService.process_uploaded_image(
            db=db,
            inspection_id=inspection_id,
            filename=file.filename or "capture.jpg",
            content=content,
            image_type=image_type,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/{inspection_id}/images",
    response_model=List[ImageResponse],
    summary="List images attached to an inspection",
)
async def list_inspection_images(
    inspection_id: str,
    db: AsyncSession = Depends(get_db),
) -> List[ImageResponse]:
    """Retrieve all images associated with an inspection session."""
    inspection = await InspectionService.get_inspection(db, inspection_id, load_relations=False)
    if not inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inspection '{inspection_id}' not found",
        )
    return await ImageService.list_images_by_inspection(db, inspection_id)
