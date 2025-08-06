from src.clean_architecture.dtos.pedido_dto import PedidoResponse
from src.clean_architecture.enums.status_pedido import StatusPedido
from src.clean_architecture.interfaces.gateways.pedido import PedidoGatewayInterface
from src.clean_architecture.use_cases.pedido.util import PedidoUtils


class ListarPedidoUseCase:
    def execute(self, pedido_gateway: PedidoGatewayInterface) -> list[PedidoResponse]:
        """
        Lista pedidos com ordenação conforme especificação da Fase 2:
        1. Pronto > Em Preparação > Recebido
        2. Pedidos mais antigos primeiro e mais novos depois
        3. Pedidos com status Finalizado não devem aparecer na lista
        """
        pedidos = pedido_gateway.listar()

        # Filtrar pedidos finalizados
        pedidos_ativos = [p for p in pedidos if p.status != StatusPedido.FINALIZADO]

        # Conforme especificação: Pronto > Em Preparação > Recebido
        prioridade_status = {
            StatusPedido.PRONTO: 1,        # Maior prioridade
            StatusPedido.PREPARANDO: 2,    # Segunda prioridade
            StatusPedido.RECEBIDO: 3,      # Terceira prioridade
            StatusPedido.PAGO: 4           # Menor prioridade (já pago mas não processado)
        }

        # Ordenar por status (prioridade) e depois por data de criação (mais antigos primeiro)
        pedidos_ordenados = sorted(
            pedidos_ativos,
            key=lambda p: (prioridade_status.get(p.status, 999), p.data_criacao)
        )

        utils = PedidoUtils()
        return [utils._to_response(p) for p in pedidos_ordenados]
