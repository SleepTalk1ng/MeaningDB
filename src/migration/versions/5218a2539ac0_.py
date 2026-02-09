"""empty message

Revision ID: 5218a2539ac0
Revises: 6954753ff272
Create Date: 2026-02-09 03:06:58.234591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5218a2539ac0'
down_revision: Union[str, Sequence[str], None] = '6954753ff272'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
