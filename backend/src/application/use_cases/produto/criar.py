from uuid import uuid4

from src.adapters.input.dto.produto_dto import ProdutoCreate, ProdutoResponse
from src.domain.models.produto import Produto
from src.ports.repositories.produto_repository_port import ProdutoRepositoryPort

class CriarProdutoUseCase:
    def __init__(self, produto_repository: ProdutoRepositoryPort):
        self.produto_repository = produto_repository

    def execute(self, produto_create: ProdutoCreate) -> ProdutoResponse:
        produto = Produto(
            id=uuid4(),
            nome=produto_create.nome,
            categoria=produto_create.categoria,
            preco=produto_create.preco
        )
        self.produto_repository.salvar(produto)
        return ProdutoResponse(**produto.__dict__)
