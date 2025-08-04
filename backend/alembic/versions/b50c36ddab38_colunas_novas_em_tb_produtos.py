"""colunas novas em tb_produtos

Revision ID: b50c36ddab38
Revises: 8c6b783e25a3
Create Date: 2025-08-04 04:50:52.356216

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b50c36ddab38'
down_revision: Union[str, None] = '8c6b783e25a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('tb_produtos', 'categoria')
    op.add_column('tb_produtos', sa.Column('categoria_id', sa.UUID(), nullable=False))
    op.add_column('tb_produtos', sa.Column('descricao', sa.String(), nullable=False))
    op.add_column('tb_produtos', sa.Column('status', sa.Boolean(), nullable=False, default=True))
    op.add_column('tb_produtos', sa.Column('imagem_url', sa.String(), nullable=True))
    op.add_column('tb_produtos', sa.Column('estoque_disponivel', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'tb_produtos', 'tb_categorias', ['categoria_id'], ['id'])


def downgrade() -> None:
    op.add_column('tb_produtos', sa.Column('categoria', sa.String(), nullable=False))
    op.drop_column('tb_produtos', 'categoria_id')
    op.drop_column('tb_produtos', 'descricao')
    op.drop_column('tb_produtos', 'estoque_disponivel')
    op.drop_column('tb_produtos', 'imagem_url')
    op.drop_column('tb_produtos', 'status')
