from abc import ABC, abstractmethod
from uuid import UUID

from src.clean_architecture.entities.pagamento import Pagamento


class PagamentoGatewayInterface(ABC):
    @abstractmethod
    def salvar(self, pagamento: Pagamento) -> Pagamento:
        pass

    @abstractmethod
    def buscar_por_id(self, pagamento_id: UUID) -> Pagamento | None:
        pass

    @abstractmethod
    def buscar_por_pedido(self, pedido_id: UUID) -> Pagamento | None:
        pass

    @abstractmethod
    def atualizar_status(self, pagamento_id: UUID, status: str) -> None:
        pass

    @abstractmethod
    def listar_por_status(self, status: str) -> list[Pagamento]:
        pass
