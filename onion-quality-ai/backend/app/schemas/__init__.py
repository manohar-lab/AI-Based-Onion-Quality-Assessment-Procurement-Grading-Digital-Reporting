"""Pydantic schemas package."""

from app.schemas.defect import (
    DefectObservationBase,
    DefectObservationCreate,
    DefectObservationResponse,
)
from app.schemas.image import (
    ImageBase,
    ImageCreate,
    ImageResponse,
)
from app.schemas.onion import (
    OnionInstanceBase,
    OnionInstanceCreate,
    OnionInstanceResponse,
)
from app.schemas.grading import (
    GradingResultBase,
    GradingResultCreate,
    GradingResultResponse,
)
from app.schemas.report import (
    QualityReportBase,
    QualityReportCreate,
    QualityReportResponse,
)
from app.schemas.inspection import (
    InspectionBase,
    InspectionCreate,
    InspectionUpdate,
    InspectionResponse,
    InspectionDetailResponse,
)

__all__ = [
    "DefectObservationBase",
    "DefectObservationCreate",
    "DefectObservationResponse",
    "ImageBase",
    "ImageCreate",
    "ImageResponse",
    "OnionInstanceBase",
    "OnionInstanceCreate",
    "OnionInstanceResponse",
    "GradingResultBase",
    "GradingResultCreate",
    "GradingResultResponse",
    "QualityReportBase",
    "QualityReportCreate",
    "QualityReportResponse",
    "InspectionBase",
    "InspectionCreate",
    "InspectionUpdate",
    "InspectionResponse",
    "InspectionDetailResponse",
]
