from uuid import UUID
from sqlalchemy.orm import Session

from src.clean_architecture.interfaces.gateways.pedido import PedidoGatewayInterface

from src.clean_architecture.entities.pedido import Pedido, ItemPedido
from src.clean_architecture.external.db.models.pedido_model import PedidoModel
from src.clean_architecture.external.db.models.item_pedido_model import ItemPedidoModel

class PedidoGateway(PedidoGatewayInterface):
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, pedido: Pedido) -> Pedido:
        pedido_model = self.db.query(PedidoModel).filter_by(id=pedido.id).first()

        if not pedido_model:
            pedido_model = PedidoModel(
                id=pedido.id,
                cliente_id=pedido.cliente_id,
                status=pedido.status,
                data_criacao=pedido.data_criacao,
            )
            self.db.add(pedido_model)
        else:
            pedido_model.status = pedido.status


        self.db.query(ItemPedidoModel).filter_by(pedido_id=pedido.id).delete()
        for item in pedido.itens:
            item_model = ItemPedidoModel(
                pedido_id=pedido.id,
                produto_id=item.produto_id,
                quantidade=item.quantidade,
            )
            self.db.add(item_model)

        self.db.commit()
        self.db.refresh(pedido_model)
        return self._converter_para_entidade(pedido_model)

    def listar(self) -> list[Pedido]:
        pedidos_model = self.db.query(PedidoModel).all()
        return [self._converter_para_entidade(p) for p in pedidos_model]

    def buscar_por_id(self, pedido_id: UUID) -> Pedido | None:
        model = self.db.query(PedidoModel).filter_by(id=pedido_id).first()
        if model:
            return self._converter_para_entidade(model)
        return None

    def deletar(self, pedido_id: UUID) -> None:
        self.db.query(ItemPedidoModel).filter_by(pedido_id=pedido_id).delete()
        self.db.query(PedidoModel).filter_by(id=pedido_id).delete()
        self.db.commit()

    def buscar_por_cliente(self, cliente_id: UUID) -> list[Pedido]:
        pedidos_model = (
            self.db.query(PedidoModel).filter_by(cliente_id=cliente_id).all()
        )
        return [self._converter_para_entidade(p) for p in pedidos_model]

    def _converter_para_entidade(self, model: PedidoModel) -> Pedido:
        itens = [
            ItemPedido(produto_id=i.produto_id, quantidade=i.quantidade)
            for i in model.itens
        ]
        return Pedido(
            id=model.id,
            cliente_id=model.cliente_id,
            status=model.status,
            data_criacao=model.data_criacao,
            itens=itens,
        )

    def atualizar_status(self, pedido_id: UUID, status: str) -> None:
        pedido_model = self.db.query(PedidoModel).filter_by(id=pedido_id).first()
        if not pedido_model:
            raise ValueError("Pedido não encontrado")
        pedido_model.status = status
        self.db.commit()
