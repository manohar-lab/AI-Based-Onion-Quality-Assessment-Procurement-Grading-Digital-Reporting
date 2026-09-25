"""Pydantic schemas for GradingResult."""

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class GradingResultBase(BaseModel):
    profile_name: str = Field(..., description="Government or agency grading profile name")
    profile_version: str = Field(..., description="Version of the grading specification")
    status: str = Field(..., description="Assigned grade or evaluation outcome")
    overall_confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence in the grading outcome")


class GradingResultCreate(GradingResultBase):
    inspection_id: str


class GradingResultResponse(GradingResultBase):
    id: str
    inspection_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(from_attributes=True)
