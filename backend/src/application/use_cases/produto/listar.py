from src.adapters.input.dto.produto_dto import ProdutoResponse
from src.ports.repositories.produto_repository_port import ProdutoRepositoryPort

class ListarProdutoUseCase:
    def __init__(self, produto_repository: ProdutoRepositoryPort):
        self.produto_repository = produto_repository

    def execute(self) -> list[ProdutoResponse]:
        produtos = self.produto_repository.listar()
        return [ProdutoResponse(**p.__dict__) for p in produtos]
