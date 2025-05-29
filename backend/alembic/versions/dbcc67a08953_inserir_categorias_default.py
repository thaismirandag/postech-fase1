"""inserir_categorias_default

Revision ID: dbcc67a08953
Revises: a500ce3feb64
Create Date: 2025-05-29 00:39:34.935711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbcc67a08953'
down_revision: Union[str, None] = 'a500ce3feb64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
