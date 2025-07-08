from src.ports.repositories.produto_repository_port import ProdutoRepositoryPort

class DeletarProdutoUseCase:
    def __init__(self, produto_repository: ProdutoRepositoryPort):
        self.produto_repository = produto_repository

    def execute(self, produto_id: str) -> None:
        self.produto_repository.deletar(produto_id)
