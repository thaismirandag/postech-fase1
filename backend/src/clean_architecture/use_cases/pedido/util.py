from src.clean_architecture.dtos.pedido_dto import PedidoResponse, ItemPedidoDTO
from src.clean_architecture.entities.pedido import Pedido

class PedidoUtils:
    def _to_response(self, pedido: Pedido) -> PedidoResponse:
        return PedidoResponse(
            id=pedido.id,
            cliente_id=pedido.cliente_id,
            status=pedido.status,
            data_criacao=pedido.data_criacao,
            itens=[
                ItemPedidoDTO(produto_id=item.produto_id, quantidade=item.quantidade)
                for item in pedido.itens
            ],
        )