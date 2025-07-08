from fastapi import HTTPException

from src.adapters.input.dto.pedido_dto import PedidoResponse
from src.application.use_cases.pedido.util import PedidoUtils
from src.ports.repositories.pedido_repository_port import PedidoRepositoryPort

class BuscarPedidoPorIDUseCase:
    def __init__(
        self,
        repository: PedidoRepositoryPort,
    ):
        self.repository = repository
    
    def execute(self, pedido_id: UUID) -> PedidoResponse:
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        return PedidoUtils._to_response(pedido)