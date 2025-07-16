from uuid import UUID, uuid4

from src.adapters.input.dto.pagamento_dto import PagamentoResponse
from src.adapters.input.dto.pedido_dto import PedidoResponse
from src.domain.models.pedido import StatusPedido
from src.ports.repositories.pedido_repository_port import PedidoRepositoryPort
from src.ports.services.pagamento_service_port import PagamentoServicePort

class GerarQRCodePagamentoUseCase:
    def __init__(self, pedido_repository: PedidoRepositoryPort):
        self._pedido_repository = pedido_repository
    
    def execute(self, pedido_id: UUID) -> PedidoResponse:
        pedido = self._pedido_repository.buscar_por_id(pedido_id)
        if not pedido:
            raise Exception("Pedido não encontrado")

        pedido.status = StatusPedido.PAGO
        self._pedido_repository.salvar(pedido)
        return pedido