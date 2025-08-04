import uuid

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

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
    descricao = Column(String, nullable=False)
    categoria_id = Column(UUID(as_uuid=True), ForeignKey('tb_categorias.id'), nullable=False)
    preco = Column(Float, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    imagem_url = Column(String, nullable=True)
    estoque_disponivel = Column(Integer, nullable=False, default=0)

    categoria = relationship("CategoriaModel", backref="produtos")

