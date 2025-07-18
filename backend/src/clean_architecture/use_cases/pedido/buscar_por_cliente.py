from uuid import UUID
from src.clean_architecture.dtos.pedido_dto import PedidoResponse
from src.clean_architecture.use_cases.pedido.util import PedidoUtils
from src.clean_architecture.interfaces.gateways.pedido import PedidoGatewayInterface

class BuscarPedidoPorClienteUseCase:
    def __init__(self, pedido_gateway: PedidoGatewayInterface):
        self.pedido_gateway = pedido_gateway

    def execute(self, cliente_id: UUID) -> list[PedidoResponse]:
        pedidos = self.pedido_gateway.buscar_por_cliente(cliente_id)
        utils = PedidoUtils()
        return [utils._to_response(p) for p in pedidos]