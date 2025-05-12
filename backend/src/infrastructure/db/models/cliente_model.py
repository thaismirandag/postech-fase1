import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from infrastructure.db.models.base import Base


class ClienteModel(Base):
    __tablename__ = "clientes"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefone = Column(String, nullable=True)
