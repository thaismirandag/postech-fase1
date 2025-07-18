from uuid import UUID
from fastapi import HTTPException

from src.clean_architecture.interfaces.gateways.pedido import PedidoGatewayInterface
from src.clean_architecture.dtos.pedido_dto import PedidoResponse
from src.clean_architecture.use_cases.pedido.util import PedidoUtils

class BuscarPedidoPorIDUseCase:
    def execute(self, pedido_id: UUID, pedido_gateway: PedidoGatewayInterface) -> PedidoResponse:
        pedido = pedido_gateway.buscar_por_id(pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        return PedidoUtils._to_response(pedido)