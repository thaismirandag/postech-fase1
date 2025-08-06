from decimal import Decimal

from src.clean_architecture.dtos.pedido_dto import PedidoCreate, PedidoResponse
from src.clean_architecture.entities.pedido import ItemPedido, Pedido
from src.clean_architecture.interfaces.gateways.fila_pedidos import (
    FilaPedidosGatewayInterface,
)
from src.clean_architecture.interfaces.gateways.pedido import PedidoGatewayInterface
from src.clean_architecture.interfaces.gateways.produto import ProdutoGatewayInterface
from src.clean_architecture.use_cases.pedido.util import PedidoUtils


class CriarPedidoUseCase:
    def execute(self, pedido_create: PedidoCreate, pedido_gateway: PedidoGatewayInterface, fila_pedido_gateway: FilaPedidosGatewayInterface, produto_gateway: ProdutoGatewayInterface) -> PedidoResponse:
        # Validação dos itens do pedido
        if not pedido_create.itens:
            raise ValueError("Pedido deve ter pelo menos um item")

        if len(pedido_create.itens) > 20:
            raise ValueError("Pedido não pode ter mais de 20 itens")

        valor_total = Decimal('0.0')
        itens_com_preco = []
        
        for item in pedido_create.itens:
            # Buscar produto para obter o preço
            produto = produto_gateway.buscar_por_id(item.produto_id)
            if not produto:
                raise ValueError(f"Produto com ID {item.produto_id} não encontrado")
            
            # Calcular subtotal do item
            subtotal_item = produto.preco * item.quantidade
            valor_total += subtotal_item
            
            # Criar item com informações do produto
            item_pedido = ItemPedido(
                produto_id=item.produto_id,
                quantidade=item.quantidade,
                produto_nome=produto.nome,
                produto_preco=produto.preco
            )
            itens_com_preco.append(item_pedido)

        # Regras de negócio: valor mínimo/máximo
        if valor_total < Decimal('5.0'):
            raise ValueError("Valor do pedido abaixo do mínimo (R$ 5,00)")
        if valor_total > Decimal('1000.0'):
            raise ValueError("Valor do pedido acima do máximo (R$ 1.000,00)")
        
        # Criação do pedido (cliente pode ser anônimo)
        pedido = Pedido.criar(
            cliente_id=pedido_create.cliente_id,
            itens=itens_com_preco,
            observacoes=pedido_create.observacoes
        )
        
        pedido = pedido_gateway.salvar(pedido)
        fila_pedido_gateway.enfileirar(pedido.id)
        utils = PedidoUtils()
        return utils._to_response(pedido)
