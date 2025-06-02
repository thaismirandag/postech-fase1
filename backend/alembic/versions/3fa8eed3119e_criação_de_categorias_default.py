"""criação de categorias default

Revision ID: 3fa8eed3119e
Revises: 312e7294b8ed
Create Date: 2025-06-02 22:10:36.579197

"""
from typing import Sequence, Union
from alembic import op
from sqlalchemy import text
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision: str = '3fa8eed3119e'
down_revision: Union[str, None] = '312e7294b8ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()

    categorias = [
        (uuid.UUID("d290f1ee-6c54-4b01-90e6-d701748f0851"), "sobremesa"),
        (uuid.UUID("e8b1d3d4-738b-4207-9b2b-2c087858d7a7"), "acompanhamento"),
        (uuid.UUID("fcab78d9-c377-41f4-bf34-03d1a8bdbd89"), "lanche"),
        (uuid.UUID("6b2e43a7-8764-48ec-8f7a-65134c8c1b9e"), "bebida"),
    ]

    for id_, nome in categorias:
        conn.execute(
            sa.text("INSERT INTO tb_categorias (id, nome) VALUES (:id, :nome)"),
            {"id": id_, "nome": nome}
        )


def downgrade():
    conn = op.get_bind()
    nomes = ["sobremesa", "acompanhamento", "lanche", "bebida"]
    for nome in nomes:
        conn.execute(
            sa.text("DELETE FROM tb_categorias WHERE nome = :nome"),
            {"nome": nome}
        )