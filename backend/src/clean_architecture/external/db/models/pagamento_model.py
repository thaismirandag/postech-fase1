import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.clean_architecture.external.db.session import Base

class PagamentoModel(Base):
    __tablename__ = "tb_pagamentos"
    __table_args__ = {'extend_existing': True}
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    pedido_id = Column(UUID(as_uuid=True), ForeignKey("tb_pedidos.id"), nullable=False)
    status = Column(String, default="pendente", nullable=False)
    data_criacao = Column(DateTime, default=datetime.now(UTC))
    data_confirmacao = Column(DateTime, nullable=True)
    qrcode_url = Column(String, nullable=True)
    qrcode_id = Column(String, nullable=True)
    external_reference = Column(String, nullable=True)
    payment_id = Column(String, nullable=True)
    valor = Column(Float, nullable=False, default=0.0)
    pedido = relationship("PedidoModel", back_populates="pagamento")


