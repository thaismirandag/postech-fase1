from abc import ABC, abstractmethod
from uuid import UUID

from src.clean_architecture.entities.fila_pedidos import FilaPedidos


class FilaPedidosGatewayInterface(ABC):
    @abstractmethod
    def enfileirar(self, pedido_id: UUID, payload: str | None = None) -> None:
        pass

    @abstractmethod
    def atualizar_status(self, pedido_id: UUID, status: str) -> None:
        pass

    @abstractmethod
    def listar_em_aberto(self) -> list[FilaPedidos]:
        pass
