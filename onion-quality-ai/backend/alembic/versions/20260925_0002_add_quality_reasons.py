"""Add quality_reasons to images table

Revision ID: 20260925_0002
Revises: 20260925_0001
Create Date: 2026-09-25 23:08:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260925_0002'
down_revision: Union[str, None] = '20260925_0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('images', sa.Column('quality_reasons', sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column('images', 'quality_reasons')
