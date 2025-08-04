from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    preco: Decimal
    categoria_id: UUID
    imagem_url: str | None = None
    estoque_disponivel: int = 0

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: UUID
