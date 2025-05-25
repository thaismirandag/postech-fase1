from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from src.adapters.input.dto.pedido_dto import PedidoCreate, PedidoResponse
from src.adapters.output.repositories.pedido_repository import PedidoRepository
from src.application.services.pedido_service import PedidoService
from src.infrastructure.db.session import get_db

router = APIRouter(prefix="/api/pedidos", tags=["Pedidos"])


# Função para injetar dependência do serviço
def get_pedido_service(db: Session = Depends(get_db)) -> PedidoService:
    repository = PedidoRepository(db)
    return PedidoService(repository)


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
