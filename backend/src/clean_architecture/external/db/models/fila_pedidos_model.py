import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from src.clean_architecture.external.db.session import Base


class FilaPedidosModel(Base):
    __tablename__ = "tb_fila_pedidos"
    __table_args__ = {'extend_existing': True}
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    status = Column(String, default="pendente", nullable=False)
    payload = Column(String, nullable=True)
