from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from src.clean_architecture.entities.produto import Produto
from src.clean_architecture.external.db.models.produto_model import ProdutoModel
from src.clean_architecture.interfaces.gateways.produto import ProdutoGatewayInterface


class ProdutoGateway(ProdutoGatewayInterface):
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_id(self, produto_id: int) -> Produto | None:
        model = self.db.query(ProdutoModel).filter_by(id=produto_id).first()
        return self._to_domain(model) if model else None

    def listar(self) -> list[Produto]:
        models = self.db.query(ProdutoModel).all()
        return [self._to_domain(m) for m in models]

    def salvar(self, produto: Produto) -> Produto:
        model = ProdutoModel(
            nome=produto.nome,
            descricao=produto.descricao,
            categoria_id=produto.categoria_id,
            preco=float(produto.preco),
            status=produto.ativo,
            imagem_url=produto.imagem_url,
            estoque_disponivel=produto.estoque_disponivel
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        produto.id = model.id
        return self._to_domain(model)

    def deletar(self, produto_id: int) -> None:
        model = self.db.query(ProdutoModel).filter_by(id=produto_id).first()
        if not model:
            raise ValueError("Produto não encontrado")
        self.db.delete(model)
        self.db.commit()

    def buscar_por_categoria(self, categoria_id: UUID) -> list[Produto]:
        models = self.db.query(ProdutoModel).filter_by(categoria_id=categoria_id).all()
        return [self._to_domain(m) for m in models]


    def _to_domain(self, model: ProdutoModel) -> Produto:
        return Produto(
            id=model.id,
            nome=model.nome,
            descricao=model.descricao,
            preco=Decimal(str(model.preco)),
            categoria_id=model.categoria_id,
            ativo=model.status,
            imagem_url=model.imagem_url,
            estoque_disponivel=model.estoque_disponivel
        )
