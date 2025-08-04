from abc import ABC, abstractmethod

from src.clean_architecture.entities.produto import Produto


class ProdutoGatewayInterface(ABC):
    @abstractmethod
    def salvar(self, produto: Produto) -> Produto:
        pass

    @abstractmethod
    def listar(self) -> list[Produto]:
        pass

    @abstractmethod
    def buscar_por_id(self, produto_id: str) -> Produto | None:
        pass

    @abstractmethod
    def deletar(self, produto_id: str) -> None:
        pass

    @abstractmethod
    def buscar_por_categoria(self, categoria: str) -> list[Produto]:
        pass
