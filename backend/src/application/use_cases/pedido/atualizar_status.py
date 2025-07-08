from uuid import UUID

from src.adapters.input.dto.pedido_dto import  PedidoResponse
from src.application.use_cases.pedido.util import PedidoUtils
from src.domain.models.pedido import StatusPedido
from src.ports.repositories.pedido_repository_port import PedidoRepositoryPort

class BuscarPedidoPorClienteUseCase:
    def __init__(
        self,
        repository: PedidoRepositoryPort,
    ):
        self.repository = repository

    def execute(self, pedido_id: UUID, novo_status: StatusPedido) -> PedidoResponse:
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            raise ValueError("Pedido não encontrado")
        pedido.status = novo_status
        pedido = self.repository.salvar(pedido)
        return PedidoUtils._to_response(pedido)