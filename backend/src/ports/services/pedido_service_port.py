from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List

from src.adapters.input.dto.pedido_dto import PedidoCreate, PedidoResponse


class PedidoServicePort(ABC):
    @abstractmethod
    def criar_pedido(self, pedido_create: PedidoCreate) -> PedidoResponse:
        pass

    @abstractmethod
    def buscar_pedido_por_id(self, pedido_id: UUID) -> Optional[PedidoResponse]:
        pass

    @abstractmethod
    def listar_pedidos(self) -> List[PedidoResponse]:
        pass

    @abstractmethod
    def deletar_pedido(self, pedido_id: UUID) -> None:
        pass

    @abstractmethod
    def buscar_pedidos_por_cliente(self, cliente_id: UUID) -> List[PedidoResponse]:
        pass
