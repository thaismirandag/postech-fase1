from uuid import UUID

from fastapi import APIRouter, Depends

from src.adapters.input.api.dependencies import get_pedido_service
from src.adapters.input.dto.pedido_dto import PedidoCreate, PedidoResponse
from src.application.services.pedido_service import PedidoService

router = APIRouter(prefix="/v1/api/public/pedidos", tags=["Painel de Pedidos"])

@router.post("/", response_model=PedidoResponse, summary="Cliente cria um pedido")
def criar_pedido(
    pedido: PedidoCreate,
    service: PedidoService = Depends(get_pedido_service),
):
    return service.criar_pedido(pedido)

@router.get("/{pedido_id}", response_model=PedidoResponse, summary="Cliente acompanha status do pedido")
def buscar_pedido(pedido_id: UUID, service: PedidoService = Depends(get_pedido_service)):
    return service.buscar_pedido_por_id(pedido_id)
