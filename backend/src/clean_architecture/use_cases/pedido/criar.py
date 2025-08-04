from src.clean_architecture.dtos.pedido_dto import PedidoCreate, PedidoResponse
from src.clean_architecture.entities.pedido import ItemPedido, Pedido
from src.clean_architecture.interfaces.gateways.fila_pedidos import (
    FilaPedidosGatewayInterface,
)
from src.clean_architecture.interfaces.gateways.pedido import PedidoGatewayInterface
from src.clean_architecture.use_cases.pedido.util import PedidoUtils


class CriarPedidoUseCase:
    def execute(self, pedido_create: PedidoCreate, pedido_gateway: PedidoGatewayInterface, fila_pedido_gateway: FilaPedidosGatewayInterface) -> PedidoResponse:
        # Validação dos itens do pedido
        if not pedido_create.itens:
            raise ValueError("Pedido deve ter pelo menos um item")

        if len(pedido_create.itens) > 20:
            raise ValueError("Pedido não pode ter mais de 20 itens")

        # Validação do valor total (mock - em produção seria calculado com preços reais)
        valor_total = sum(item.quantidade for item in pedido_create.itens) * 10.0

        # Regras de negócio: valor mínimo/máximo
        if valor_total < 5.0:
            raise ValueError("Valor do pedido abaixo do mínimo (R$ 5,00)")
        if valor_total > 1000.0:
            raise ValueError("Valor do pedido acima do máximo (R$ 1.000,00)")

        # Criação dos itens
        itens = [
            ItemPedido(produto_id=item.produto_id, quantidade=item.quantidade)
            for item in pedido_create.itens
        ]
        pedido = Pedido.criar(cliente_id=pedido_create.cliente_id, itens=itens)
        pedido = pedido_gateway.salvar(pedido)
        fila_pedido_gateway.enfileirar(pedido.id)
        utils = PedidoUtils()
        return utils._to_response(pedido)
