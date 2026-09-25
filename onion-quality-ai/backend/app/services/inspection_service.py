"""Inspection CRUD and business logic service."""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.inspection import Inspection
from app.models.image import Image
from app.models.onion import OnionInstance
from app.schemas.inspection import InspectionCreate, InspectionUpdate


class InspectionService:
    """Service layer encapsulating database access for Inspections."""

    @staticmethod
    async def create_inspection(
        db: AsyncSession,
        payload: InspectionCreate,
    ) -> Inspection:
        """Create and persist a new inspection session."""
        inspection = Inspection(
            lot_id=payload.lot_id,
            status="pending",
            grading_profile=payload.grading_profile,
        )
        db.add(inspection)
        await db.flush()
        await db.refresh(inspection)
        return inspection

    @staticmethod
    async def get_inspection(
        db: AsyncSession,
        inspection_id: str,
        load_relations: bool = True,
    ) -> Optional[Inspection]:
        """Fetch an inspection by primary key, optionally eagerly loading related entities."""
        query = select(Inspection).where(Inspection.id == inspection_id)
        if load_relations:
            query = query.options(
                selectinload(Inspection.images),
                selectinload(Inspection.onion_instances).selectinload(OnionInstance.defect_observations),
                selectinload(Inspection.grading_results),
                selectinload(Inspection.quality_reports),
            )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def list_inspections(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        lot_id: Optional[str] = None,
    ) -> List[Inspection]:
        """List inspections with pagination and optional lot_id filtering."""
        query = select(Inspection).order_by(Inspection.created_at.desc())
        if lot_id:
            query = query.where(Inspection.lot_id == lot_id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def update_inspection(
        db: AsyncSession,
        inspection: Inspection,
        payload: InspectionUpdate,
    ) -> Inspection:
        """Update inspection status or grading profile."""
        if payload.status is not None:
            inspection.status = payload.status
        if payload.grading_profile is not None:
            inspection.grading_profile = payload.grading_profile
        await db.flush()
        await db.refresh(inspection)
        return inspection
