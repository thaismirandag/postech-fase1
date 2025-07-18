from uuid import UUID, uuid4
from src.clean_architecture.dtos.pagamento_dto import PagamentoResponse
from src.clean_architecture.dtos.pedido_dto import PedidoResponse
from src.clean_architecture.enums.status_pedido import StatusPedido
from src.clean_architecture.interfaces.gateways.pedido import PedidoGatewayInterface

class ConfirmarPagamentoUseCase:
    def __init__(self, pedido_gateway: PedidoGatewayInterface):
        self._pedido_gateway = pedido_gateway
    
    def execute(self, pedido_id: UUID) -> PedidoResponse:
        pedido = self._pedido_gateway.buscar_por_id(pedido_id)
        if not pedido:
            raise Exception("Pedido não encontrado")
        
        # Validação de status - verificar se pode ser pago
        if pedido.status not in [StatusPedido.RECEBIDO]:
            raise ValueError("Pedido não pode ser pago no status atual")
        
        pedido.atualizar_status(StatusPedido.PAGO)
        pedido = self._pedido_gateway.salvar(pedido)
        return pedido