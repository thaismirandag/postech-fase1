from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.clean_architecture.external.db.session import get_db
from src.clean_architecture.api.security.jwt_handler import get_current_admin 
from src.clean_architecture.dtos.pedido_dto import AtualizarStatusPedidoDTO, PedidoResponse
from src.clean_architecture.controllers.fila_pedidos import FilaPedidosController
from src.clean_architecture.controllers.pedido import PedidoController

router = APIRouter(prefix="/v1/api/admin/pedidos", tags=["Painel administrativo de Pedidos"], dependencies=[Depends(get_current_admin)])

@router.get("/em-aberto", response_model=list[PedidoResponse], summary="Listar pedidos em aberto")
def listar_pedidos_em_aberto(db: Session = Depends(get_db)):
    fila = FilaPedidosController.listar_em_aberto(db)
    pedidos = []
    for f in fila:
        pedido = PedidoController.buscar_por_id(f.id, db)
        if pedido:
            pedidos.append(pedido)
    return pedidos

@router.patch("/{pedido_id}/status", response_model=PedidoResponse, summary="Atualizar status do pedido")
def atualizar_status_pedido( pedido_id: UUID, dto: AtualizarStatusPedidoDTO , db: Session = Depends(get_db)):
    return PedidoController.atualizar_status_pedido(pedido_id, dto.status)

@router.get("/", response_model=list[PedidoResponse], summary="Listar todos os pedidos")
def listar_pedidos(db: Session = Depends(get_db)):
    return PedidoController.listar_pedidos(db)

@router.delete("/{pedido_id}", status_code=204, summary="Deletar pedido")
def deletar_pedido(pedido_id: UUID, db: Session = Depends(get_db)):
    PedidoController.deletar_pedido(pedido_id, db)
