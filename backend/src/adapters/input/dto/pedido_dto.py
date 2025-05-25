from uuid import UUID
from datetime import datetime
from typing import List

from pydantic import BaseModel


class ItemPedidoDTO(BaseModel):
    produto_id: UUID
    quantidade: int


class PedidoCreate(BaseModel):
    cliente_id: UUID
    itens: List[ItemPedidoDTO]


class PedidoResponse(BaseModel):
    id: UUID
    cliente_id: UUID
    status: str
    data_criacao: datetime
    itens: List[ItemPedidoDTO]
