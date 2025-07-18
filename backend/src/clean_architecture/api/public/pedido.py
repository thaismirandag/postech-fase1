from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.clean_architecture.dtos.pedido_dto import PedidoCreate, PedidoResponse
from src.clean_architecture.controllers.pedido import PedidoController

from src.clean_architecture.external.db.session import get_db

router = APIRouter(prefix="/v1/api/public/pedidos", tags=["Painel de Pedidos"])

@router.post("/", response_model=PedidoResponse, summary="Cliente cria um pedido")
def criar_pedido( pedido: PedidoCreate, db: Session = Depends(get_db) ):
    return PedidoController.criar_pedido(pedido, db)

@router.get("/{pedido_id}", response_model=PedidoResponse, summary="Cliente acompanha status do pedido")
def buscar_pedido(pedido_id: UUID, db: Session = Depends(get_db)):
    return PedidoController.buscar_por_id(pedido_id, db)
