from src.clean_architecture.interfaces.gateways.fila_pedidos import FilaPedidosGatewayInterface

class ListaPedidosEmabertoUseCase:
    def execute(gateway: FilaPedidosGatewayInterface):
        return gateway.listar_em_aberto()