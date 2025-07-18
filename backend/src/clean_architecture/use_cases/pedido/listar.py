from src.clean_architecture.dtos.pedido_dto import PedidoResponse
from src.clean_architecture.use_cases.pedido.util import PedidoUtils
from src.clean_architecture.interfaces.gateways.pedido import PedidoGatewayInterface

class ListarPedidoUseCase:
    def execute(self, pedido_gateway: PedidoGatewayInterface) -> list[PedidoResponse]:
        pedidos = pedido_gateway.listar()
        return [PedidoUtils._to_response(p) for p in pedidos]