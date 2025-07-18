from uuid import UUID
from sqlalchemy.orm import Session

from src.clean_architecture.interfaces.gateways.fila_pedidos import FilaPedidosGatewayInterface

from src.clean_architecture.external.db.models.fila_pedidos_model import FilaPedidosModel
from src.clean_architecture.entities.fila_pedidos import FilaPedidos

from src.clean_architecture.enums.status_pedido import StatusPedido

class FilaPedidosGateway(FilaPedidosGatewayInterface):
    def __init__(self, db: Session):
        self.db = db

    def enfileirar(self, pedido_id: UUID, payload: str | None = None) -> None:
        fila = FilaPedidosModel(id=pedido_id, status=StatusPedido.RECEBIDO.value, payload=payload)
        self.db.add(fila)
        self.db.commit()

    def atualizar_status(self, pedido_id: UUID, status: str) -> None:
        fila = self.db.query(FilaPedidosModel).filter_by(id=pedido_id).first()
        if fila:
            fila.status = status
            self.db.commit()

    def listar_em_aberto(self) -> list[FilaPedidos]:
        registros = self.db.query(FilaPedidosModel).filter(
            FilaPedidosModel.status != StatusPedido.FINALIZADO.value
        ).all()
        return [FilaPedidos(id=r.id, status=StatusPedido(r.status), payload=r.payload) for r in registros]