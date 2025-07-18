from src.clean_architecture.interfaces.gateways.fila_pedidos import FilaPedidosGatewayInterface

class ListaPedidosEmabertoUseCase:
    def execute(self, gateway: FilaPedidosGatewayInterface):
        return gateway.listar_em_aberto()