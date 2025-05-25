from typing import List, Optional
from uuid import UUID
from datetime import datetime

from src.adapters.input.dto.pedido_dto import (
    PedidoCreate,
    PedidoResponse,
    ItemPedidoDTO,
)
from src.domain.models.pedido import Pedido, ItemPedido
from src.ports.repositories.pedido_repository_port import PedidoRepositoryPort
from src.ports.services.pedido_service_port import PedidoServicePort


class PedidoService(PedidoServicePort):
    def __init__(self, repository: PedidoRepositoryPort):
        self.repository = repository

    def criar_pedido(self, pedido_create: PedidoCreate) -> PedidoResponse:
        # Converte os itens do DTO para objetos de domínio
        itens = [
            ItemPedido(produto_id=item.produto_id, quantidade=item.quantidade)
            for item in pedido_create.itens
        ]

        pedido = Pedido.criar(cliente_id=pedido_create.cliente_id, itens=itens)

        pedido = self.repository.salvar(pedido)
        return self._to_response(pedido)

    def buscar_pedido_por_id(self, pedido_id: UUID) -> Optional[PedidoResponse]:
        pedido = self.repository.buscar_por_id(pedido_id)
        if pedido:
            return self._to_response(pedido)
        return None

    def listar_pedidos(self) -> List[PedidoResponse]:
        pedidos = self.repository.listar()
        return [self._to_response(p) for p in pedidos]

    def deletar_pedido(self, pedido_id: UUID) -> None:
        self.repository.deletar(pedido_id)

    def buscar_pedidos_por_cliente(self, cliente_id: UUID) -> List[PedidoResponse]:
        pedidos = self.repository.buscar_por_cliente(cliente_id)
        return [self._to_response(p) for p in pedidos]

    def _to_response(self, pedido: Pedido) -> PedidoResponse:
        return PedidoResponse(
            id=pedido.id,
            cliente_id=pedido.cliente_id,
            status=pedido.status,
            data_criacao=pedido.data_criacao,
            itens=[
                ItemPedidoDTO(produto_id=item.produto_id, quantidade=item.quantidade)
                for item in pedido.itens
            ],
        )
