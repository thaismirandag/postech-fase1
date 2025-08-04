from src.clean_architecture.dtos.pedido_dto import CheckoutPedidoRequest, PedidoResponse
from src.clean_architecture.entities.pedido import ItemPedido, Pedido
from src.clean_architecture.interfaces.gateways.fila_pedidos import (
    FilaPedidosGatewayInterface,
)
from src.clean_architecture.interfaces.gateways.pedido import PedidoGatewayInterface
from src.clean_architecture.use_cases.pedido.util import PedidoUtils


class CheckoutPedidoUseCase:
    def execute(self, checkout_request: CheckoutPedidoRequest, pedido_gateway: PedidoGatewayInterface, fila_pedido_gateway: FilaPedidosGatewayInterface) -> PedidoResponse:
        """
        Checkout de pedido - Fase 2
        Recebe os produtos solicitados e retorna a identificação do pedido
        """
        # Validação dos itens do pedido
        if not checkout_request.itens:
            raise ValueError("Pedido deve ter pelo menos um item")

        if len(checkout_request.itens) > 20:
            raise ValueError("Pedido não pode ter mais de 20 itens")

        # Validação do valor total (mock - em produção seria calculado com preços reais)
        valor_total = sum(item.quantidade for item in checkout_request.itens) * 10.0

        # Regras de negócio: valor mínimo/máximo
        if valor_total < 5.0:
            raise ValueError("Valor do pedido abaixo do mínimo (R$ 5,00)")
        if valor_total > 1000.0:
            raise ValueError("Valor do pedido acima do máximo (R$ 1.000,00)")

        # Criação dos itens
        itens = [
            ItemPedido(produto_id=item.produto_id, quantidade=item.quantidade)
            for item in checkout_request.itens
        ]

        # Criação do pedido (cliente pode ser anônimo)
        pedido = Pedido.criar(
            cliente_id=checkout_request.cliente_id,
            itens=itens,
            observacoes=checkout_request.observacoes
        )

        # Salvar pedido e enfileirar
        pedido = pedido_gateway.salvar(pedido)
        fila_pedido_gateway.enfileirar(pedido.id)

        utils = PedidoUtils()
        return utils._to_response(pedido)
