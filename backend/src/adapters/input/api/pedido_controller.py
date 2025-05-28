from uuid import UUID

from fastapi import APIRouter, Depends

from src.adapters.input.api.dependencies import get_pedido_service
from src.adapters.input.dto.pedido_dto import (
    AtualizarStatusPedidoDTO,
    PedidoCreate,
    PedidoResponse,
)
from src.application.services.pedido_service import PedidoService

router = APIRouter(prefix="/api/pedidos", tags=["Pedidos"])


@router.post("/", response_model=PedidoResponse, summary="Criar Pedido")
def criar_pedido(
    pedido: PedidoCreate,
    service: PedidoService = Depends(get_pedido_service),
):
    return service.criar_pedido(pedido)


@router.get("/", response_model=list[PedidoResponse], summary="Listar Pedidos")
def listar_pedidos(
    service: PedidoService = Depends(get_pedido_service),
):
    return service.listar_pedidos()


@router.get(
    "/{pedido_id}", response_model=PedidoResponse, summary="Buscar Pedido por ID"
)
def buscar_pedido(
    pedido_id: UUID,
    service: PedidoService = Depends(get_pedido_service),
):
    return service.buscar_pedido_por_id(pedido_id)


@router.get(
    "/cliente/{cliente_id}",
    response_model=list[PedidoResponse],
    summary="Buscar Pedidos por Cliente",
)
def buscar_pedidos_por_cliente(
    cliente_id: UUID,
    service: PedidoService = Depends(get_pedido_service),
):
    return service.buscar_pedidos_por_cliente(cliente_id)


@router.delete("/{pedido_id}", status_code=204, summary="Deletar Pedido")
def deletar_pedido(
    pedido_id: UUID,
    service: PedidoService = Depends(get_pedido_service),
):
    service.deletar_pedido(pedido_id)


@router.patch("/{pedido_id}/status", response_model=PedidoResponse, summary="Atualizar Status do Pedido")
def atualizar_status_pedido(
    pedido_id: UUID,
    dto: AtualizarStatusPedidoDTO,
    service: PedidoService = Depends(get_pedido_service),
):
    return service.atualizar_status_pedido(pedido_id, dto.status)
