"""add column user_name

Revision ID: 339b014dcb32
Revises: 
Create Date: 2025-10-01 13:30:20.770716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '339b014dcb32'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("loans",sa.Column("user_name",sa.String(30)))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("loans","user_name")