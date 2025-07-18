from uuid import UUID

from src.clean_architecture.interfaces.gateways.pedido import PedidoGatewayInterface
from src.clean_architecture.dtos.pedido_dto import PedidoResponse
from src.clean_architecture.use_cases.pedido.util import PedidoUtils
from src.clean_architecture.enums.status_pedido import StatusPedido

class AtualizarStatusPedidoUseCase:
    def execute(self, pedido_id: UUID, novo_status: StatusPedido, pedido_gateway: PedidoGatewayInterface) -> PedidoResponse:
        pedido = pedido_gateway.buscar_por_id(pedido_id)
        if not pedido:
            raise ValueError("Pedido não encontrado")
        pedido.status = novo_status
        pedido = pedido_gateway.salvar(pedido)
        utils = PedidoUtils()
        return utils._to_response(pedido)