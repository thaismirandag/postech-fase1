from uuid import UUID

from src.clean_architecture.interfaces.gateways.pedido import PedidoGatewayInterface


class DeletarPedidoUseCase:
    def execute(self, pedido_id: UUID, pedido_gateway: PedidoGatewayInterface) -> None:
        pedido_gateway.deletar(pedido_id)
