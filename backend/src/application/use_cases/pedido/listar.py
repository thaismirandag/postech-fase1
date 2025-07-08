from src.adapters.input.dto.pedido_dto import PedidoResponse
from src.ports.repositories.pedido_repository_port import PedidoRepositoryPort

class ListarPedidoUseCase:
    def __init__(
        self,
        repository: PedidoRepositoryPort,
    ):
        self.repository = repository
    
    def execute(self) -> list[PedidoResponse]:
        pedidos = self.repository.listar()
        return [self._to_response(p) for p in pedidos]