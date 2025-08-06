"""adicionar_campo_observacoes_pedidos

Revision ID: 9c4a9953f05f
Revises: b50c36ddab38
Create Date: 2025-08-05 21:07:15.045642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c4a9953f05f'
down_revision: Union[str, None] = 'b50c36ddab38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('tb_pedidos', sa.Column('observacoes', sa.String(), nullable=True))
    op.alter_column('tb_pedidos', 'cliente_id',
                    existing_type=sa.UUID(),
                    nullable=True)
    op.alter_column('tb_pedidos', 'status',
                    existing_type=sa.Enum('pendente', 'em_preparo', 'pronto', 'entregue', 'cancelado', name='statuspedido'),
                    nullable=True)


def downgrade() -> None:
    op.drop_column('tb_pedidos', 'observacoes')	
    op.alter_column('tb_pedidos', 'cliente_id',
                    existing_type=sa.UUID(),
                    nullable=False)
    op.alter_column('tb_pedidos', 'status',
                    existing_type=sa.Enum('pendente', 'em_preparo', 'pronto', 'entregue', 'cancelado', name='statuspedido'),
                    nullable=False)