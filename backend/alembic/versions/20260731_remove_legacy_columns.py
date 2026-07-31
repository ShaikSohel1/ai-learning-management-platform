"""Remove legacy columns from enrollments and certificates tables

Revision ID: 20260731_remove_legacy_columns
Revises: 164183281d0a
Create Date: 2026-07-31 10:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260731_remove_legacy_columns'
down_revision: Union[str, None] = '164183281d0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Safely drop obsolete legacy columns not present in SQLAlchemy models
    with op.batch_alter_table('enrollments', schema=None) as batch_op:
        batch_op.drop_column('progress')
        batch_op.drop_column('enrolled_at')

    with op.batch_alter_table('certificates', schema=None) as batch_op:
        batch_op.drop_column('expiry_date')


def downgrade() -> None:
    # Re-add columns if downgraded
    with op.batch_alter_table('certificates', schema=None) as batch_op:
        batch_op.add_column(sa.Column('expiry_date', sa.DATE(), nullable=True))

    with op.batch_alter_table('enrollments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('enrolled_at', sa.DATE(), nullable=True))
        batch_op.add_column(sa.Column('progress', sa.INTEGER(), nullable=True))
