"""Initial inspection and quality assessment tables

Revision ID: 20260925_0001
Revises: 
Create Date: 2026-09-25 23:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260925_0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. inspections
    op.create_table(
        'inspections',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('lot_id', sa.String(length=100), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('grading_profile', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_inspections_lot_id'), 'inspections', ['lot_id'], unique=False)
    op.create_index(op.f('ix_inspections_status'), 'inspections', ['status'], unique=False)

    # 2. images
    op.create_table(
        'images',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('inspection_id', sa.String(length=36), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('image_type', sa.String(length=50), nullable=False),
        sa.Column('capture_timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('quality_status', sa.String(length=50), nullable=False),
        sa.Column('quality_score', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['inspection_id'], ['inspections.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_images_inspection_id'), 'images', ['inspection_id'], unique=False)

    # 3. onion_instances
    op.create_table(
        'onion_instances',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('inspection_id', sa.String(length=36), nullable=False),
        sa.Column('image_id', sa.String(length=36), nullable=True),
        sa.Column('bounding_box', sa.JSON(), nullable=True),
        sa.Column('segmentation_path', sa.String(length=500), nullable=True),
        sa.Column('detection_confidence', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['inspection_id'], ['inspections.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_onion_instances_inspection_id'), 'onion_instances', ['inspection_id'], unique=False)
    op.create_index(op.f('ix_onion_instances_image_id'), 'onion_instances', ['image_id'], unique=False)

    # 4. defect_observations
    op.create_table(
        'defect_observations',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('onion_id', sa.String(length=36), nullable=False),
        sa.Column('defect_type', sa.String(length=100), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('severity', sa.String(length=50), nullable=True),
        sa.Column('evidence_path', sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(['onion_id'], ['onion_instances.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_defect_observations_onion_id'), 'defect_observations', ['onion_id'], unique=False)

    # 5. grading_results
    op.create_table(
        'grading_results',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('inspection_id', sa.String(length=36), nullable=False),
        sa.Column('profile_name', sa.String(length=100), nullable=False),
        sa.Column('profile_version', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('overall_confidence', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['inspection_id'], ['inspections.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_grading_results_inspection_id'), 'grading_results', ['inspection_id'], unique=False)

    # 6. quality_reports
    op.create_table(
        'quality_reports',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('inspection_id', sa.String(length=36), nullable=False),
        sa.Column('report_path', sa.String(length=500), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['inspection_id'], ['inspections.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_quality_reports_inspection_id'), 'quality_reports', ['inspection_id'], unique=False)


def downgrade() -> None:
    op.drop_table('quality_reports')
    op.drop_table('grading_results')
    op.drop_table('defect_observations')
    op.drop_table('onion_instances')
    op.drop_table('images')
    op.drop_table('inspections')
