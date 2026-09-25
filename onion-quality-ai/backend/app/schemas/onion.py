"""Pydantic schemas for OnionInstance."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.defect import DefectObservationResponse


class OnionInstanceBase(BaseModel):
    bounding_box: Optional[Dict[str, Any]] = Field(None, description="Bounding box coordinates (x, y, w, h)")
    segmentation_path: Optional[str] = Field(None, description="Path to saved segmentation mask")
    detection_confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Detection confidence score")


class OnionInstanceCreate(OnionInstanceBase):
    inspection_id: str
    image_id: Optional[str] = None


class OnionInstanceResponse(OnionInstanceBase):
    id: str
    inspection_id: str
    image_id: Optional[str] = None
    defect_observations: List[DefectObservationResponse] = []

    model_config = ConfigDict(from_attributes=True)
