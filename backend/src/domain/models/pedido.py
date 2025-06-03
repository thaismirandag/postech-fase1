from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.domain.models.item_pedido import ItemPedido
from src.domain.models.status_pedido import StatusPedido


class Pedido:
    def __init__(
        self,
        id: UUID,
        cliente_id: UUID | None,
        status: StatusPedido = StatusPedido.RECEBIDO,
        data_criacao: datetime | None = None,
        itens: list[ItemPedido] | None = None,
    ):
        self.id = id
        self.cliente_id = cliente_id
        self.status = status
        self.data_criacao = data_criacao or datetime.now(UTC)
        self.itens = itens or []

    @classmethod
    def criar(cls, cliente_id: UUID, itens: list["ItemPedido"]) -> "Pedido":
        return cls(
            id=uuid4(),
            cliente_id=cliente_id,
            status=StatusPedido.RECEBIDO,
            data_criacao=datetime.now(UTC),
            itens=itens,
        )
