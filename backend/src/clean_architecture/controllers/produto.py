from uuid import UUID

from sqlalchemy.orm import Session

from src.clean_architecture.dtos.produto_dto import ProdutoCreate
from src.clean_architecture.gateways.produto import ProdutoGateway
from src.clean_architecture.use_cases.produto.criar import CriarProdutoUseCase
from src.clean_architecture.use_cases.produto.deletar import DeletarProdutoUseCase
from src.clean_architecture.use_cases.produto.listar import ListarProdutoUseCase


class ProdutoController:
    def criar_produto(dto: ProdutoCreate, db: Session):
        produto_gateway = ProdutoGateway(db)
        use_case = CriarProdutoUseCase()
        return use_case.execute(dto, produto_gateway)

    def listar_produtos(db: Session):
        produto_gateway = ProdutoGateway(db)
        use_case = ListarProdutoUseCase()
        return use_case.execute(produto_gateway)

    def deletar_produto(produto_id: UUID, db: Session):
        produto_gateway = ProdutoGateway(db)
        use_case = DeletarProdutoUseCase()
        return use_case.execute(produto_id, produto_gateway)
