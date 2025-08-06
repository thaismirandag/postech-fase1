from abc import ABC, abstractmethod
from uuid import UUID

from src.clean_architecture.entities.produto import Produto


class ProdutoGatewayInterface(ABC):
    @abstractmethod
    def salvar(self, produto: Produto) -> Produto:
        pass

    @abstractmethod
    def listar(self) -> list[Produto]:
        pass

    @abstractmethod
    def buscar_por_id(self, produto_id: UUID) -> Produto | None:
        pass

    @abstractmethod
    def deletar(self, produto_id: UUID) -> None:
        pass

    @abstractmethod
    def buscar_por_categoria(self, categoria_id: UUID) -> list[Produto]:
        pass
