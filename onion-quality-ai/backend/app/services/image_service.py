"""Image ingestion, storage, and retrieval service."""

from datetime import datetime, timezone
import os
from pathlib import Path
import re
from typing import List, Optional, Set
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.image import Image
from app.schemas.image import ImageCreate
from app.services.image_quality_service import ImageQualityService

settings = get_settings()


class ImageService:
    """Service encapsulating storage, quality gating, and database access for images."""

    ALLOWED_EXTENSIONS: Set[str] = {".jpg", ".jpeg", ".png"}
    ALLOWED_MIME_TYPES: Set[str] = {"image/jpeg", "image/png"}

    @classmethod
    def generate_safe_filename(cls, original_filename: str) -> str:
        """Sanitize filename and prepend unique timestamp + UUID prefix to avoid collisions."""
        ext = Path(original_filename).suffix.lower()
        if ext not in cls.ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file extension '{ext}'. Allowed extensions: {', '.join(cls.ALLOWED_EXTENSIONS)}"
            )
        # Strip path traversal and special characters from stem
        safe_stem = re.sub(r"[^a-zA-Z0-9_\-]", "_", Path(original_filename).stem)[:30]
        unique_token = uuid.uuid4().hex[:12]
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        return f"{timestamp}_{unique_token}_{safe_stem}{ext}"

    @classmethod
    async def process_uploaded_image(
        cls,
        db: AsyncSession,
        inspection_id: str,
        filename: str,
        content: bytes,
        image_type: str = "capture",
    ) -> Image:
        """Store original image to disk, evaluate quality gates, and record metadata."""
        # 1. Generate safe unique filename
        safe_name = cls.generate_safe_filename(filename)

        # 2. Ensure target storage directory exists
        storage_base = Path(settings.image_directory) / "inspections" / inspection_id
        storage_base.mkdir(parents=True, exist_ok=True)
        file_path = storage_base / safe_name

        # 3. Store raw original image
        with open(file_path, "wb") as f:
            f.write(content)

        # 4. Evaluate quality metrics (blur, exposure, resolution)
        quality_eval = ImageQualityService.evaluate(content)

        # 5. Persist metadata to database
        image = Image(
            inspection_id=inspection_id,
            file_path=str(file_path.as_posix()),
            image_type=image_type,
            capture_timestamp=datetime.now(timezone.utc),
            quality_status=quality_eval.quality_status,
            quality_score=quality_eval.quality_score,
            quality_reasons=quality_eval.quality_reasons,
        )
        db.add(image)
        await db.flush()
        await db.refresh(image)
        return image

    @staticmethod
    async def add_image(
        db: AsyncSession,
        inspection_id: str,
        payload: ImageCreate,
    ) -> Image:
        """Directly insert an image record (e.g., from mock or existing file path)."""
        image = Image(
            inspection_id=inspection_id,
            file_path=payload.file_path,
            image_type=payload.image_type,
            capture_timestamp=payload.capture_timestamp or datetime.now(timezone.utc),
            quality_status=payload.quality_status,
            quality_score=payload.quality_score,
            quality_reasons=payload.quality_reasons or [],
        )
        db.add(image)
        await db.flush()
        await db.refresh(image)
        return image

    @staticmethod
    async def list_images_by_inspection(
        db: AsyncSession,
        inspection_id: str,
    ) -> List[Image]:
        """Fetch all images registered under a specific inspection."""
        query = (
            select(Image)
            .where(Image.inspection_id == inspection_id)
            .order_by(Image.capture_timestamp.asc())
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_image(
        db: AsyncSession,
        image_id: str,
    ) -> Optional[Image]:
        """Fetch a single image by primary key."""
        query = select(Image).where(Image.id == image_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
