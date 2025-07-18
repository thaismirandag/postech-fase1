from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.clean_architecture.external.db.session import get_db
from src.clean_architecture.api.security.jwt_handler import get_current_admin 
from src.clean_architecture.dtos.pedido_dto import AtualizarStatusPedidoDTO, PedidoResponse, PedidoCreate, CheckoutPedidoRequest
from src.clean_architecture.controllers.fila_pedidos import FilaPedidosController
from src.clean_architecture.controllers.pedido import PedidoController

router = APIRouter(prefix="/v1/api/admin/pedidos", tags=["Painel de Pedidos"])

# Rotas públicas (sem autenticação)
@router.post("/", response_model=PedidoResponse, summary="Cliente cria um pedido")
def criar_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    return PedidoController.criar_pedido(pedido, db)

@router.post("/checkout", response_model=PedidoResponse, summary="Checkout do pedido - Fase 2")
def checkout_pedido(checkout_request: CheckoutPedidoRequest, db: Session = Depends(get_db)):
    """Checkout de pedido conforme especificação da Fase 2"""
    return PedidoController.checkout_pedido(checkout_request, db)

@router.get("/{pedido_id}", response_model=PedidoResponse, summary="Cliente acompanha status do pedido")
def buscar_pedido(pedido_id: UUID, db: Session = Depends(get_db)):
    return PedidoController.buscar_por_id(pedido_id, db)

# Rotas administrativas (com autenticação)
@router.get("/em-aberto", response_model=list[PedidoResponse], summary="Listar pedidos em aberto", dependencies=[Depends(get_current_admin)])
def listar_pedidos_em_aberto(db: Session = Depends(get_db)):
    fila = FilaPedidosController.listar_em_aberto(db)
    pedidos = []
    for f in fila:
        pedido = PedidoController.buscar_por_id(f.id, db)
        if pedido:
            pedidos.append(pedido)
    return pedidos

@router.patch("/{pedido_id}/status", response_model=PedidoResponse, summary="Atualizar status do pedido", dependencies=[Depends(get_current_admin)])
def atualizar_status_pedido(pedido_id: UUID, dto: AtualizarStatusPedidoDTO, db: Session = Depends(get_db)):
    return PedidoController.atualizar_status_pedido(pedido_id, dto.status)

@router.get("/", response_model=list[PedidoResponse], summary="Listar todos os pedidos", dependencies=[Depends(get_current_admin)])
def listar_pedidos(db: Session = Depends(get_db)):
    return PedidoController.listar_pedidos(db)

@router.delete("/{pedido_id}", status_code=204, summary="Deletar pedido", dependencies=[Depends(get_current_admin)])
def deletar_pedido(pedido_id: UUID, db: Session = Depends(get_db)):
    PedidoController.deletar_pedido(pedido_id, db)
