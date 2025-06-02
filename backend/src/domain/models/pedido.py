from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID

from src.domain.models.status_pedido import StatusPedido
from src.domain.models.item_pedido import ItemPedido

class Pedido:
    def __init__(
        self,
        id: UUID,
        cliente_id: Optional[UUID],
        status: StatusPedido = StatusPedido.RECEBIDO,
        data_criacao: Optional[datetime] = None,
        itens: Optional[List[ItemPedido]] = None,
    ):
        self.id = id
        self.cliente_id = cliente_id
        self.status = status
        self.data_criacao = data_criacao or datetime.now(timezone.utc)
        self.itens = itens or []

