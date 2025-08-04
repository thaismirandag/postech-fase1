import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.clean_architecture.external.db.session import Base


class ClienteModel(Base):
    __tablename__ = "tb_clientes"
    __table_args__ = {'extend_existing': True}
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    nome = Column(String, nullable=True)
    cpf = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    pedidos = relationship("PedidoModel", back_populates="cliente")

