from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.clean_architecture.external.db.session import get_db
from src.clean_architecture.dtos.cliente_dto import ClienteCreate, ClienteResponse
from src.clean_architecture.controllers.cliente import ClienteController

router = APIRouter(prefix="/v1/api/public/clientes",tags=["Painel de Clientes"])

@router.post("/", response_model=ClienteResponse, summary="Criar ou obter cliente")
def criar_ou_obter_cliente( dto: ClienteCreate, db: Session = Depends(get_db) ):
    return ClienteController.criar_ou_obter_cliente(dto, db)
