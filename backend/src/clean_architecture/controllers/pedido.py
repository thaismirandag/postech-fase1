from uuid import UUID

from sqlalchemy.orm import Session

from src.clean_architecture.dtos.pedido_dto import CheckoutPedidoRequest, PedidoCreate
from src.clean_architecture.enums.status_pedido import StatusPedido
from src.clean_architecture.gateways.fila_pedidos import FilaPedidosGateway
from src.clean_architecture.gateways.pedido import PedidoGateway
from src.clean_architecture.use_cases.pedido.atualizar_status import (
    AtualizarStatusPedidoUseCase,
)
from src.clean_architecture.use_cases.pedido.buscar_por_id import (
    BuscarPedidoPorIDUseCase,
)
from src.clean_architecture.use_cases.pedido.checkout import CheckoutPedidoUseCase
from src.clean_architecture.use_cases.pedido.criar import CriarPedidoUseCase
from src.clean_architecture.use_cases.pedido.deletar import DeletarPedidoUseCase
from src.clean_architecture.use_cases.pedido.listar import ListarPedidoUseCase


class PedidoController:
    def criar_pedido(pedido: PedidoCreate, db: Session):
        pedido_gateway = PedidoGateway(db)
        fila_pedido_gateway = FilaPedidosGateway(db)
        use_case = CriarPedidoUseCase()
        return use_case.execute(pedido, pedido_gateway, fila_pedido_gateway)

    def checkout_pedido(checkout_request: CheckoutPedidoRequest, db: Session):
        """Checkout de pedido - Fase 2"""
        pedido_gateway = PedidoGateway(db)
        fila_pedido_gateway = FilaPedidosGateway(db)
        use_case = CheckoutPedidoUseCase()
        return use_case.execute(checkout_request, pedido_gateway, fila_pedido_gateway)

    def buscar_por_id(id: UUID, db: Session):
        pedido_gateway = PedidoGateway(db)
        use_case = BuscarPedidoPorIDUseCase()
        return use_case.execute(id, pedido_gateway)

    def atualizar_status_pedido(pedido_id: UUID, new_status: StatusPedido, db: Session):
        pedido_gateway = PedidoGateway(db)
        use_case = AtualizarStatusPedidoUseCase()
        return use_case.execute(pedido_id, new_status, pedido_gateway)

    def listar_pedidos(db: Session):
        pedido_gateway = PedidoGateway(db)
        use_case = ListarPedidoUseCase()
        return use_case.execute(pedido_gateway)

    def deletar_pedido(pedido_id: UUID, db: Session):
        pedido_gateway = PedidoGateway(db)
        use_case = DeletarPedidoUseCase()
        return use_case.execute(pedido_id, pedido_gateway)
