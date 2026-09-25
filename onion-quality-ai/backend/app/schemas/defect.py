"""Pydantic schemas for DefectObservation."""

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class DefectObservationBase(BaseModel):
    defect_type: str = Field(..., description="Type of defect (e.g., rot, sprout, mechanical_damage)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")
    severity: Optional[str] = Field(None, description="Severity grade (minor, moderate, severe)")
    evidence_path: Optional[str] = Field(None, description="Path to cropped defect evidence image")


class DefectObservationCreate(DefectObservationBase):
    onion_id: str = Field(..., description="Target onion instance ID")


class DefectObservationResponse(DefectObservationBase):
    id: str
    onion_id: str

    model_config = ConfigDict(from_attributes=True)
