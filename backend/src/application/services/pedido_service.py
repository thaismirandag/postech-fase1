from uuid import UUID
from src.adapters.input.dto.pedido_dto import (
    ItemPedidoDTO,
    PedidoCreate,
    PedidoResponse,
)
from src.domain.models.pedido import ItemPedido, Pedido, StatusPedido
from src.ports.repositories.pedido_repository_port import PedidoRepositoryPort
from src.ports.repositories.fila_pedidos_repository_port import FilaPedidosRepositoryPort
from src.ports.services.pedido_service_port import PedidoServicePort


class PedidoService(PedidoServicePort):
    def __init__(
        self,
        repository: PedidoRepositoryPort,
        fila_repository: FilaPedidosRepositoryPort,
    ):
        self.repository = repository
        self.fila_repository = fila_repository

    def criar_pedido(self, pedido_create: PedidoCreate) -> PedidoResponse:
        itens = [
            ItemPedido(produto_id=item.produto_id, quantidade=item.quantidade)
            for item in pedido_create.itens
        ]

        pedido = Pedido.criar(cliente_id=pedido_create.cliente_id, itens=itens)
        pedido = self.repository.salvar(pedido)
        self.fila_repository.enfileirar(pedido.id)  # integração com fila

        return self._to_response(pedido)

    def buscar_pedido_por_id(self, pedido_id: UUID) -> PedidoResponse | None:
        pedido = self.repository.buscar_por_id(pedido_id)
        if pedido:
            return self._to_response(pedido)
        return None

    def listar_pedidos(self) -> list[PedidoResponse]:
        pedidos = self.repository.listar()
        return [self._to_response(p) for p in pedidos]

    def deletar_pedido(self, pedido_id: UUID) -> None:
        self.repository.deletar(pedido_id)

    def buscar_pedidos_por_cliente(self, cliente_id: UUID) -> list[PedidoResponse]:
        pedidos = self.repository.buscar_por_cliente(cliente_id)
        return [self._to_response(p) for p in pedidos]

    def atualizar_status_pedido(self, pedido_id: UUID, novo_status: StatusPedido) -> PedidoResponse:
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            raise ValueError("Pedido não encontrado")

        pedido.status = novo_status
        pedido = self.repository.salvar(pedido)
        return self._to_response(pedido)

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
