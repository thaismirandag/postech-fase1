import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base

class PedidoModel(Base):
    __tablename__ = "pedidos"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    status = Column(String, default="pendente", nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    itens = relationship("ItemPedidoModel", back_populates="pedido")

class ItemPedidoModel(Base):
    __tablename__ = "itens_pedido"
    pedido_id = Column(UUID(as_uuid=True), ForeignKey("pedidos.id"), primary_key=True)
    produto_id = Column(UUID(as_uuid=True), ForeignKey("produtos.id"), primary_key=True)
    quantidade = Column(String, nullable=False)
    pedido = relationship("PedidoModel", back_populates="itens")

class FilaPedidosModel(Base):
    __tablename__ = "fila_pedidos"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    status = Column(String, default="pendente", nullable=False)
    payload = Column(String, nullable=True)
