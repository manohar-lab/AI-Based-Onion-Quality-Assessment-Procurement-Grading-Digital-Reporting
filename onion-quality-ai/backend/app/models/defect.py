"""DefectObservation ORM model."""

from typing import Optional, TYPE_CHECKING
import uuid

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.onion import OnionInstance


class DefectObservation(Base):
    """Represents a defect observed on an individual onion."""

    __tablename__ = "defect_observations"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    onion_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("onion_instances.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    defect_type: Mapped[str] = mapped_column(String(100), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    evidence_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    onion_instance: Mapped["OnionInstance"] = relationship(
        "OnionInstance",
        back_populates="defect_observations",
    )
