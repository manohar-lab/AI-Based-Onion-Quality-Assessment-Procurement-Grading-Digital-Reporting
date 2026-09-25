"""Inspection ORM model."""

from datetime import datetime, timezone
from typing import List, TYPE_CHECKING
import uuid

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.image import Image
    from app.models.onion import OnionInstance
    from app.models.grading import GradingResult
    from app.models.report import QualityReport


class Inspection(Base):
    """Represents a lot inspection session for onion quality assessment."""

    __tablename__ = "inspections"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    lot_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True)
    grading_profile: Mapped[str] = mapped_column(String(100), nullable=False, default="AGMARK_2024_v1")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    images: Mapped[List["Image"]] = relationship(
        "Image",
        back_populates="inspection",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    onion_instances: Mapped[List["OnionInstance"]] = relationship(
        "OnionInstance",
        back_populates="inspection",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    grading_results: Mapped[List["GradingResult"]] = relationship(
        "GradingResult",
        back_populates="inspection",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    quality_reports: Mapped[List["QualityReport"]] = relationship(
        "QualityReport",
        back_populates="inspection",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
