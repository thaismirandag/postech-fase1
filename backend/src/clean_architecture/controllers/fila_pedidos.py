from sqlalchemy.orm import Session

from src.clean_architecture.gateways.fila_pedidos import FilaPedidosGateway
from src.clean_architecture.use_cases.fila_pedidos.listar_em_aberto import ListaPedidosEmabertoUseCase

class FilaPedidosController:
    def listar_em_aberto(db: Session):
        gateway = FilaPedidosGateway(db)
        use_case = ListaPedidosEmabertoUseCase()
        return use_case.execute(gateway)