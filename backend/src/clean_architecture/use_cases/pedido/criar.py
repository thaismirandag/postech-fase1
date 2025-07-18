from src.clean_architecture.dtos.pedido_dto import PedidoCreate, PedidoResponse
from src.clean_architecture.entities.pedido import ItemPedido, Pedido

from src.clean_architecture.use_cases.pedido.util import PedidoUtils

from src.clean_architecture.interfaces.gateways.pedido import PedidoGatewayInterface
from src.clean_architecture.interfaces.gateways.fila_pedidos import FilaPedidosGatewayInterface

class CriarPedidoUseCase:
    def execute(self, pedido_create: PedidoCreate, pedido_gateway: PedidoGatewayInterface, fila_pedido_gateway: FilaPedidosGatewayInterface) -> PedidoResponse:
        itens = [
            ItemPedido(produto_id=item.produto_id, quantidade=item.quantidade)
            for item in pedido_create.itens
        ]

        pedido = Pedido.criar(cliente_id=pedido_create.cliente_id, itens=itens)
        pedido = pedido_gateway.salvar(pedido)
        fila_pedido_gateway.enfileirar(pedido.id)

        return PedidoUtils._to_response(pedido)