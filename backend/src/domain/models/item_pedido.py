from uuid import UUID
from dataclasses import dataclass

@dataclass
class ItemPedido:
    produto_id: UUID
    quantidade: int

