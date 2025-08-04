from uuid import UUID

from sqlalchemy.orm import Session

from src.clean_architecture.entities.pedido import ItemPedido, Pedido
from src.clean_architecture.external.db.models.cliente_model import ClienteModel
from src.clean_architecture.external.db.models.item_pedido_model import ItemPedidoModel
from src.clean_architecture.external.db.models.pedido_model import PedidoModel
from src.clean_architecture.external.db.models.produto_model import ProdutoModel
from src.clean_architecture.interfaces.gateways.pedido import PedidoGatewayInterface


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
                observacoes=pedido.observacoes,
            )
            self.db.add(pedido_model)
        else:
            pedido_model.status = pedido.status
            pedido_model.observacoes = pedido.observacoes

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
        """Lista pedidos com informações completas de produtos e clientes"""
        pedidos_model = (
            self.db.query(PedidoModel)
            .join(ClienteModel, PedidoModel.cliente_id == ClienteModel.id)
            .all()
        )
        return [self._converter_para_entidade(p) for p in pedidos_model]

    def buscar_por_id(self, pedido_id: UUID) -> Pedido | None:
        model = (
            self.db.query(PedidoModel)
            .join(ClienteModel, PedidoModel.cliente_id == ClienteModel.id)
            .filter_by(id=pedido_id)
            .first()
        )
        if model:
            return self._converter_para_entidade(model)
        return None

    def deletar(self, pedido_id: UUID) -> None:
        self.db.query(ItemPedidoModel).filter_by(pedido_id=pedido_id).delete()
        self.db.query(PedidoModel).filter_by(id=pedido_id).delete()
        self.db.commit()

    def buscar_por_cliente(self, cliente_id: UUID) -> list[Pedido]:
        pedidos_model = (
            self.db.query(PedidoModel)
            .join(ClienteModel, PedidoModel.cliente_id == ClienteModel.id)
            .filter_by(cliente_id=cliente_id)
            .all()
        )
        return [self._converter_para_entidade(p) for p in pedidos_model]

    def _converter_para_entidade(self, model: PedidoModel) -> Pedido:
        # Buscar itens com informações dos produtos
        itens_com_produtos = (
            self.db.query(ItemPedidoModel, ProdutoModel)
            .join(ProdutoModel, ItemPedidoModel.produto_id == ProdutoModel.id)
            .filter_by(pedido_id=model.id)
            .all()
        )

        itens = [
            ItemPedido(
                produto_id=item.produto_id,
                quantidade=item.quantidade,
                produto_nome=produto.nome,
                produto_preco=produto.preco
            )
            for item, produto in itens_com_produtos
        ]

        return Pedido(
            id=model.id,
            cliente_id=model.cliente_id,
            cliente_nome=model.cliente.nome if model.cliente else None,
            status=model.status,
            data_criacao=model.data_criacao,
            itens=itens,
            observacoes=model.observacoes,
        )

    def atualizar_status(self, pedido_id: UUID, status: str) -> None:
        pedido_model = self.db.query(PedidoModel).filter_by(id=pedido_id).first()
        if not pedido_model:
            raise ValueError("Pedido não encontrado")
        pedido_model.status = status
        self.db.commit()
