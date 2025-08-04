from src.clean_architecture.dtos.pedido_dto import ItemPedidoResponseDTO, PedidoResponse
from src.clean_architecture.entities.pedido import Pedido


class PedidoUtils:
    def _to_response(self, pedido: Pedido) -> PedidoResponse:
        return PedidoResponse(
            id=pedido.id,
            cliente_id=pedido.cliente_id,
            cliente_nome=pedido.cliente_nome,
            status=pedido.status,
            data_criacao=pedido.data_criacao,
            valor_total=pedido.calcular_total(),
            observacoes=pedido.observacoes,
            itens=[
                ItemPedidoResponseDTO(
                    produto_id=item.produto_id,
                    produto_nome=item.produto_nome or "Produto não encontrado",
                    produto_preco=item.produto_preco or 0.0,
                    quantidade=item.quantidade,
                    subtotal=item.calcular_subtotal()
                )
                for item in pedido.itens
            ],
        )
