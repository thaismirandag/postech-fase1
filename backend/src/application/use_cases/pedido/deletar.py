from uuid import UUID

from src.ports.repositories.pedido_repository_port import PedidoRepositoryPort

class ListarPedidoUseCase:
    def __init__(
        self,
        repository: PedidoRepositoryPort,
    ):
        self.repository = repository
    
    def execute(self, pedido_id: UUID) -> None:
        self.repository.deletar(pedido_id)