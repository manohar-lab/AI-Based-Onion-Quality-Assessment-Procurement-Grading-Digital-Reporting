"""Pydantic schemas for QualityReport."""

from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field


class QualityReportBase(BaseModel):
    report_path: str = Field(..., description="File path or URL of the generated report")


class QualityReportCreate(QualityReportBase):
    inspection_id: str


class QualityReportResponse(QualityReportBase):
    id: str
    inspection_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(from_attributes=True)
