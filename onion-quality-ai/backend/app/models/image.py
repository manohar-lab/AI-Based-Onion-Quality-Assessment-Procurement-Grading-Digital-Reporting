"""Image ORM model."""

from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
import uuid

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.inspection import Inspection
    from app.models.onion import OnionInstance


class Image(Base):
    """Represents an image captured or uploaded for an inspection."""

    __tablename__ = "images"

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
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    image_type: Mapped[str] = mapped_column(String(50), nullable=False, default="capture")
    capture_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    quality_status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    quality_reasons: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True, default=list)

    # Relationships
    inspection: Mapped["Inspection"] = relationship("Inspection", back_populates="images")
    onion_instances: Mapped[List["OnionInstance"]] = relationship(
        "OnionInstance",
        back_populates="image",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
