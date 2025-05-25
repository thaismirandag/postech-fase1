from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from src.domain.models.pedido import Pedido


class PedidoRepositoryPort(ABC):
    @abstractmethod
    def salvar(self, pedido: Pedido) -> Pedido:
        pass

    @abstractmethod
    def listar(self) -> List[Pedido]:
        pass

    @abstractmethod
    def buscar_por_id(self, pedido_id: UUID) -> Optional[Pedido]:
        pass

    @abstractmethod
    def deletar(self, pedido_id: UUID) -> None:
        pass

    @abstractmethod
    def buscar_por_cliente(self, cliente_id: UUID) -> List[Pedido]:
        pass