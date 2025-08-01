"""adicionar_campos_mercadopago

Revision ID: mercadopago_integration
Revises: 6d0212687665
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'mercadopago_integration'
down_revision = '6d0212687665'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_pagamentos', sa.Column('qrcode_url', sa.String(), nullable=True))
    op.add_column('tb_pagamentos', sa.Column('qrcode_id', sa.String(), nullable=True))
    op.add_column('tb_pagamentos', sa.Column('external_reference', sa.String(), nullable=True))
    op.add_column('tb_pagamentos', sa.Column('payment_id', sa.String(), nullable=True))
    op.add_column('tb_pagamentos', sa.Column('valor', sa.Float(), nullable=False, server_default='0.0'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tb_pagamentos', 'valor')
    op.drop_column('tb_pagamentos', 'payment_id')
    op.drop_column('tb_pagamentos', 'external_reference')
    op.drop_column('tb_pagamentos', 'qrcode_id')
    op.drop_column('tb_pagamentos', 'qrcode_url')
    # ### end Alembic commands ### 