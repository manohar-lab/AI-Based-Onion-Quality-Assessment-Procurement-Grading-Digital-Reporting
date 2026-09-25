"""Pydantic schemas for Image."""

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ImageBase(BaseModel):
    file_path: str = Field(..., description="File system or storage path of the image")
    image_type: str = Field(default="capture", description="Image modality or angle (e.g., top_view, tray, single)")
    capture_timestamp: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the image was captured",
    )
    quality_status: str = Field(default="pending", description="Image quality gate status (passed, recapture, pending)")
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Quality assessment score")
    quality_reasons: list[str] = Field(
        default_factory=list,
        description="Actionable reasons explaining quality evaluation or why recapture is recommended",
    )


class ImageCreate(ImageBase):
    pass


class ImageResponse(ImageBase):
    id: str
    inspection_id: str

    model_config = ConfigDict(from_attributes=True)
