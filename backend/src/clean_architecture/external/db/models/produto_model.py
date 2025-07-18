import uuid

from sqlalchemy import Column, Float, String
from sqlalchemy.dialects.postgresql import UUID

from src.clean_architecture.external.db.session import Base

class ProdutoModel(Base):
    __tablename__ = "tb_produtos"
    __table_args__ = {'extend_existing': True}
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    preco = Column(Float, nullable=False)

