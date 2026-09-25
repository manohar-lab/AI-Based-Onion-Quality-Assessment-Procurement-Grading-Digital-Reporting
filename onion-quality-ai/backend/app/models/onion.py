"""OnionInstance ORM model."""

from typing import Any, Dict, List, Optional, TYPE_CHECKING
import uuid

from sqlalchemy import Float, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.inspection import Inspection
    from app.models.image import Image
    from app.models.defect import DefectObservation


class OnionInstance(Base):
    """Represents an individual onion detected in an image/inspection."""

    __tablename__ = "onion_instances"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    inspection_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("inspections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    image_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("images.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    bounding_box: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    segmentation_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    detection_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relationships
    inspection: Mapped["Inspection"] = relationship("Inspection", back_populates="onion_instances")
    image: Mapped[Optional["Image"]] = relationship("Image", back_populates="onion_instances")
    defect_observations: Mapped[List["DefectObservation"]] = relationship(
        "DefectObservation",
        back_populates="onion_instance",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
