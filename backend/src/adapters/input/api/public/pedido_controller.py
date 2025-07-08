from uuid import UUID

from fastapi import APIRouter, Depends

from src.adapters.input.dto.pedido_dto import PedidoCreate, PedidoResponse
from src.application.use_cases.pedido.buscar_por_id import BuscarPedidoPorIDUseCase
from src.application.use_cases.pedido.criar import CriarPedidoUseCase

router = APIRouter(prefix="/v1/api/public/pedidos", tags=["Painel de Pedidos"])

@router.post("/", response_model=PedidoResponse, summary="Cliente cria um pedido")
def criar_pedido(
    pedido: PedidoCreate,
    criarPedidoUseCase: CriarPedidoUseCase
):
    return criarPedidoUseCase.execute(pedido)

@router.get("/{pedido_id}", response_model=PedidoResponse, summary="Cliente acompanha status do pedido")
def buscar_pedido(
        pedido_id: UUID,
        buscarPedidoPorIDUseCase: BuscarPedidoPorIDUseCase
    ):
    
    return buscarPedidoPorIDUseCase.execute(pedido_id)
