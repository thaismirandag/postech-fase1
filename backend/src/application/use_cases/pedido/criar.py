from src.adapters.input.dto.pedido_dto import (
    PedidoCreate,
    PedidoResponse,
)
from src.application.use_cases.pedido.util import PedidoUtils
from src.domain.models.pedido import ItemPedido, Pedido
from src.ports.repositories.fila_pedidos_repository_port import (
    FilaPedidosRepositoryPort,
)
from src.ports.repositories.pedido_repository_port import PedidoRepositoryPort

class CriarPedidoUseCase:
    def __init__(
        self,
        repository: PedidoRepositoryPort,
        fila_repository: FilaPedidosRepositoryPort,
    ):
        self.repository = repository
        self.fila_repository = fila_repository
    
    def execute(self, pedido_create: PedidoCreate) -> PedidoResponse:
        itens = [
            ItemPedido(produto_id=item.produto_id, quantidade=item.quantidade)
            for item in pedido_create.itens
        ]

        pedido = Pedido.criar(cliente_id=pedido_create.cliente_id, itens=itens)
        pedido = self.repository.salvar(pedido)
        self.fila_repository.enfileirar(pedido.id)

        return PedidoUtils._to_response(pedido)