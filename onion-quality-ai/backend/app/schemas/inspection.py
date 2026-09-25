"""Pydantic schemas for Inspection."""

from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.image import ImageResponse
from app.schemas.onion import OnionInstanceResponse
from app.schemas.grading import GradingResultResponse
from app.schemas.report import QualityReportResponse


class InspectionBase(BaseModel):
    lot_id: str = Field(..., min_length=1, max_length=100, description="Lot/batch identifier for procurement")
    grading_profile: str = Field(
        default="AGMARK_2024_v1",
        description="Versioned government grading profile to apply",
    )


class InspectionCreate(InspectionBase):
    pass


class InspectionUpdate(BaseModel):
    status: Optional[str] = Field(None, description="Updated inspection status")
    grading_profile: Optional[str] = Field(None, description="Updated grading profile")


class InspectionResponse(InspectionBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InspectionDetailResponse(InspectionResponse):
    images: List[ImageResponse] = []
    onion_instances: List[OnionInstanceResponse] = []
    grading_results: List[GradingResultResponse] = []
    quality_reports: List[QualityReportResponse] = []

    model_config = ConfigDict(from_attributes=True)
