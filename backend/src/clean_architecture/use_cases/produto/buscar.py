from src.adapters.input.dto.produto_dto import ProdutoResponse
from src.ports.repositories.produto_repository_port import ProdutoRepositoryPort

class BuscarProdutoUseCase:
    def __init__(self, produto_repository: ProdutoRepositoryPort):
        self.produto_repository = produto_repository

    def execute(self, produto_id: str) -> ProdutoResponse | None:
        produto = self.produto_repository.buscar_por_id(produto_id)
        if produto:
            return ProdutoResponse(**produto.__dict__)
        return None
