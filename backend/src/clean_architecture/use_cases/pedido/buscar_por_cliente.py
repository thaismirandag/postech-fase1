from uuid import UUID

from src.adapters.input.dto.pedido_dto import PedidoResponse
from src.application.use_cases.pedido.util import PedidoUtils
from src.ports.repositories.pedido_repository_port import PedidoRepositoryPort

class BuscarPedidoPorClienteUseCase:
    def __init__(
        self,
        repository: PedidoRepositoryPort,
    ):
        self.repository = repository

    def execute(self, cliente_id: UUID) -> list[PedidoResponse]:
        pedidos = self.repository.buscar_por_cliente(cliente_id)
        return [PedidoUtils._to_response(p) for p in pedidos]